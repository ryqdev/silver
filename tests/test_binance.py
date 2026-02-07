import json
import sys
import types
import unittest
import importlib


def load_binance_module():
    websockets_stub = types.SimpleNamespace(
        WebSocketServerProtocol=object,
        exceptions=types.SimpleNamespace(ConnectionClosed=Exception),
    )
    sys.modules.setdefault("websockets", websockets_stub)
    return importlib.import_module("src.binance")


BinanceWebSocket = load_binance_module().BinanceWebSocket


class RecordingBinanceWebSocket(BinanceWebSocket):
    def __init__(self):
        super().__init__()
        self.ticker_payloads = []
        self.kline_payloads = []

    def handle_ticker_data(self, data):
        self.ticker_payloads.append(data)

    def handle_kline_data(self, data):
        self.kline_payloads.append(data)


class TestBinanceWebSocketMessages(unittest.IsolatedAsyncioTestCase):
    async def test_handle_message_subscription_confirmation(self):
        ws = RecordingBinanceWebSocket()

        await ws.handle_message(json.dumps({"result": None, "id": 1}))

        self.assertEqual(ws.ticker_payloads, [])
        self.assertEqual(ws.kline_payloads, [])

    async def test_handle_message_raw_ticker_event(self):
        ws = RecordingBinanceWebSocket()

        payload = {"e": "24hrTicker", "s": "BTCUSDT", "c": "20000", "v": "100"}
        await ws.handle_message(json.dumps(payload))

        self.assertEqual(ws.ticker_payloads, [payload])
        self.assertEqual(ws.kline_payloads, [])

    async def test_handle_message_raw_kline_event(self):
        ws = RecordingBinanceWebSocket()

        payload = {
            "e": "kline",
            "k": {"s": "BTCUSDT", "c": "21000", "v": "50"},
        }
        await ws.handle_message(json.dumps(payload))

        self.assertEqual(ws.ticker_payloads, [])
        self.assertEqual(ws.kline_payloads, [payload])

    async def test_handle_message_combined_stream_events(self):
        ws = RecordingBinanceWebSocket()

        ticker_payload = {"e": "24hrTicker", "s": "ETHUSDT", "c": "1800", "v": "10"}
        ticker_message = {"stream": "ethusdt@ticker", "data": ticker_payload}
        await ws.handle_message(json.dumps(ticker_message))

        kline_payload = {"e": "kline", "s": "ETHUSDT", "c": "1750", "v": "20"}
        kline_message = {"stream": "ethusdt@kline_1m", "data": kline_payload}
        await ws.handle_message(json.dumps(kline_message))

        self.assertEqual(ws.ticker_payloads, [ticker_payload])
        self.assertEqual(ws.kline_payloads, [kline_payload])

    async def test_handle_message_invokes_callback(self):
        ws = RecordingBinanceWebSocket()
        captured = []

        def callback(data):
            captured.append(data)

        payload = {"e": "24hrTicker", "s": "BTCUSDT", "c": "20000", "v": "100"}
        await ws.handle_message(json.dumps(payload), callback=callback)

        self.assertEqual(captured, [payload])
