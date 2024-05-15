from typing import NoReturn
import yfinance as yf
import pandas as pd
from loguru import logger


def handle_csv(symbol: str) -> NoReturn:
    logger.info(f"handle_csv {symbol}")

    df_list = []
    data = yf.download(symbol, group_by="Ticker", period='max')
    df_list.append(data)

    df = pd.concat(df_list)
    df.to_csv(f'data/{symbol}.csv')




