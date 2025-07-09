from loguru import logger

def start(symbol: str, start: str, end: str, kline: str) -> None:
    logger.info(f"starting with {symbol}, start: {start}, end: {end}, kline: {kline}")