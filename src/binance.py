import asyncio
import websockets
import json
import time
from loguru import logger
from typing import Optional, Callable, Dict, Any

class BinanceWebSocket:
    def __init__(self):
        self.base_url = "wss://stream.binance.com:9443/ws"
        # This is a client connection, not a server protocol.
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.subscriptions = []
        self.running = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 10
        self.reconnect_delay = 1
        self.max_reconnect_delay = 60
        self.ping_interval = 30
        self.last_ping = time.time()
        
    async def connect(self):
        """Connect to Binance WebSocket stream"""
        try:
            self.websocket = await websockets.connect(
                self.base_url,
                ping_interval=self.ping_interval,
                ping_timeout=10,
                close_timeout=10
            )
            self.running = True
            self.reconnect_attempts = 0
            self.last_ping = time.time()
            logger.info("Connected to Binance WebSocket")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
            
    async def reconnect(self):
        """Reconnect with exponential backoff"""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            logger.error(f"Max reconnection attempts ({self.max_reconnect_attempts}) reached")
            return False
            
        delay = min(self.reconnect_delay * (2 ** self.reconnect_attempts), self.max_reconnect_delay)
        self.reconnect_attempts += 1
        
        logger.info(f"Reconnecting in {delay} seconds (attempt {self.reconnect_attempts}/{self.max_reconnect_attempts})")
        await asyncio.sleep(delay)
        
        try:
            await self.connect()
            await self.resubscribe()
            return True
        except Exception as e:
            logger.error(f"Reconnection attempt {self.reconnect_attempts} failed: {e}")
            return False
            
    async def resubscribe(self):
        """Resubscribe to all previous subscriptions after reconnection"""
        if not self.subscriptions:
            return
            
        logger.info("Resubscribing to previous streams...")
        for i, stream_name in enumerate(self.subscriptions):
            try:
                subscription_msg = {
                    "method": "SUBSCRIBE",
                    "params": [stream_name],
                    "id": i + 1
                }
                await self.websocket.send(json.dumps(subscription_msg))
                logger.info(f"Resubscribed to: {stream_name}")
            except Exception as e:
                logger.error(f"Failed to resubscribe to {stream_name}: {e}")
            
    async def subscribe_ticker(self, symbol: str = "btcusdt"):
        """Subscribe to ticker stream for a symbol"""
        stream_name = f"{symbol.lower()}@ticker"
        self.subscriptions.append(stream_name)
        
        subscription_msg = {
            "method": "SUBSCRIBE",
            "params": [stream_name],
            "id": len(self.subscriptions)
        }
        
        await self.websocket.send(json.dumps(subscription_msg))
        logger.info(f"Subscribed to ticker stream: {stream_name}")
        
    async def subscribe_kline(self, symbol: str = "btcusdt", interval: str = "1h"):
        """Subscribe to kline/candlestick stream for a symbol"""
        stream_name = f"{symbol.lower()}@kline_{interval}"
        self.subscriptions.append(stream_name)
        
        subscription_msg = {
            "method": "SUBSCRIBE", 
            "params": [stream_name],
            "id": len(self.subscriptions)
        }
        
        await self.websocket.send(json.dumps(subscription_msg))
        logger.info(f"Subscribed to kline stream: {stream_name}")
        
    async def handle_message(self, message: str, callback: Optional[Callable] = None):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            
            # Handle subscription confirmations
            if "result" in data and "id" in data:
                logger.info(f"Subscription confirmed for ID {data['id']}")
                return
            
            # Handle direct event messages (raw WebSocket format)
            if "e" in data:
                event_type = data["e"]
                if event_type == "24hrTicker":
                    self.handle_ticker_data(data)
                elif event_type == "kline":
                    self.handle_kline_data(data)
                    
            # Handle combined stream format (if using /stream endpoint)
            elif "stream" in data:
                stream_data = data["data"]
                stream_name = data["stream"]
                
                if "@ticker" in stream_name:
                    self.handle_ticker_data(stream_data)
                elif "@kline" in stream_name:
                    self.handle_kline_data(stream_data)
                    
            if callback:
                callback(data)
                    
        except json.JSONDecodeError:
            logger.error(f"Failed to parse message: {message}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            
    def handle_ticker_data(self, data: Dict[str, Any]):
        """Process ticker data"""
        logger.info(f"Ticker - Symbol: {data['s']}, Price: {data['c']}, Volume: {data['v']}")
        
    def handle_kline_data(self, data: Dict[str, Any]):
        """Process kline data"""
        if 'k' in data:
            # Raw WebSocket format
            kline = data['k']
            logger.info(f"Kline - Symbol: {kline['s']}, Close: {kline['c']}, Volume: {kline['v']}")
        else:
            # Combined stream format
            logger.info(f"Kline - Symbol: {data['s']}, Close: {data['c']}, Volume: {data['v']}")
        
    async def listen(self, callback: Optional[Callable] = None):
        """Listen for incoming messages with automatic reconnection"""
        logger.info("Starting to listen for messages...")
        consecutive_errors = 0
        max_consecutive_errors = 5
        while self.running:
            try:
                if self.websocket is None or self.websocket.close_code is not None:
                    logger.warning("WebSocket is closed, attempting to reconnect...")
                    success = await self.reconnect()
                    if not success:
                        logger.error("Failed to reconnect, stopping listener")
                        break
                    continue

                message = await asyncio.wait_for(self.websocket.recv(), timeout=self.ping_interval + 10)
                logger.debug(f"Received raw message: {message}")
                await self.handle_message(message, callback)
                consecutive_errors = 0

            except websockets.exceptions.ConnectionClosed:
                logger.warning("WebSocket connection closed, attempting to reconnect...")
                success = await self.reconnect()
                if not success:
                    logger.error("Failed to reconnect, stopping listener")
                    break
                    
            except asyncio.TimeoutError:
                logger.warning("No message received within timeout, checking connection...")
                try:
                    await self.websocket.ping()
                    self.last_ping = time.time()
                except Exception as e:
                    logger.error(f"Ping failed: {e}, attempting to reconnect...")
                    success = await self.reconnect()
                    if not success:
                        logger.error("Failed to reconnect, stopping listener")
                        break
                        
            except Exception as e:
                # Unexpected error: retry a few times, but don't loop forever
                # on a persistent failure (e.g. a bug in message handling).
                consecutive_errors += 1
                logger.error(
                    f"Error receiving message "
                    f"({consecutive_errors}/{max_consecutive_errors}): {e}"
                )
                if consecutive_errors >= max_consecutive_errors:
                    logger.error("Too many consecutive errors, stopping listener")
                    break
                await asyncio.sleep(1)
                
    def is_connected(self) -> bool:
        """Check if WebSocket is connected"""
        return self.websocket is not None and self.websocket.close_code is None and self.running
        
    async def close(self):
        """Close WebSocket connection"""
        self.running = False
        if self.websocket and self.websocket.close_code is None:
            try:
                await self.websocket.close()
                logger.info("WebSocket connection closed gracefully")
            except Exception as e:
                logger.error(f"Error closing WebSocket: {e}")
        self.websocket = None


async def main():
    """Example usage with improved error handling"""
    ws = BinanceWebSocket()
    
    try:
        await ws.connect()
        await ws.subscribe_ticker("btcusdt")
        await ws.subscribe_kline("btcusdt", "1m")
        
        logger.info("Starting WebSocket listener with automatic reconnection...")
        await ws.listen()
        
    except KeyboardInterrupt:
        logger.info("Stopping...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        await ws.close()
        logger.info("Application stopped")


if __name__ == "__main__":
    asyncio.run(main())