import datetime
import os

import pandas

import clickhouse_connect
import yfinance as yf
import pandas as pd

from typing import NoReturn, List
from loguru import logger
from dotenv import load_dotenv


def handle_data(symbol: str) -> NoReturn:
    logger.info(f"handler_data {symbol}")
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="max")

    clickhouse_client = get_clickhouse_client()
    write_clickhouse(clickhouse_client, symbol, hist)
    # read_clickhouse(clickhouse_client)


def get_clickhouse_client():
    load_dotenv()
    client = clickhouse_connect.get_client(
        host='famep8kcv5.ap-southeast-1.aws.clickhouse.cloud',
        user='default',
        password=os.getenv('CLICKHOUSE_PASSWORD'),
        secure=True
    )
    return client


def write_clickhouse(client, symbol: str, data: pandas.DataFrame) -> NoReturn:
    client.command(
        f'DROP TABLE {symbol}')
    client.command(
        f'CREATE TABLE IF NOT EXISTS {symbol} (Date Date, Open Float64, High Float64, Low Float64, Close Float64, Volume Int64, Dividends Float64, Stock_Splits Float64) ENGINE = MergeTree() ORDER BY Date PRIMARY KEY Date')

    clickhouse_data = []
    for index, row in data.iterrows():
        year = int(index.strftime('%Y'))
        month = int(index.strftime('%m'))
        day = int(index.strftime('%d'))
        record = [datetime.date(year, month, day), row['Open'], row['High'], row['Low'], row['Close'],
                  int(row['Volume']), row['Dividends'], row['Stock Splits']]
        clickhouse_data.append(record)

    client.insert(symbol, clickhouse_data)


def read_clickhouse(client, symbol: str, date: str) -> List:
    ddl = f"select * from {symbol} where Date == '{date}'"
    result = client.query(ddl)
    return result.result_rows


def save_to_csv(df_list, symbol):
    df = pd.concat(df_list)
    df.to_csv(f'{symbol}.csv')
