from typing import NoReturn, List
import yfinance as yf
import pandas as pd
from loguru import logger


def handle_csv(symbol: str) -> NoReturn:
    logger.info(f"handle_csv {symbol}")

    data: pd.DataFrame = yf.download(symbol, group_by="Ticker", period='max')

    data.to_csv(f'data/{symbol}.csv')
