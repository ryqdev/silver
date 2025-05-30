import os

import yfinance as yf
import pandas as pd

from loguru import logger

def handle_csv(symbol: str) -> None:
    logger.info(f"handle_csv {symbol}")

    data: pd.DataFrame = yf.download(symbol, group_by="Ticker", period='max')
    if not os.path.exists("data"):
        os.makedirs("data")

    data.to_csv(f'data/{symbol}.csv')
