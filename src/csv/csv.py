from typing import NoReturn
import yfinance as yf
import pandas as pd
from loguru import logger


def handle_csv(symbol: str) -> NoReturn:
    logger.info(f"handle_csv {symbol}")
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="max")
    save_to_csv(hist, symbol)



def save_to_csv(df_list, symbol):
    df = pd.concat(df_list)
    df.to_csv(f'{symbol}.csv')
