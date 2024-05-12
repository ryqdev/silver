import argparse
import datetime
import os
from typing import NoReturn

import pandas
from dotenv import load_dotenv

import clickhouse_connect
import yfinance as yf
import pandas as pd


def main() -> NoReturn:
    parser = argparse.ArgumentParser(description='silver')
    parser.add_argument('--data',
                        type=str,
                        help='fetch data',
                        default='SPY')
    parser.add_argument('--backtest',
                        type=str,
                        help='backtest strategies',
                        default='SPY')

    args = parser.parse_args()
    symbol: str = args.data

    ticker = yf.Ticker(symbol)

    hist = ticker.history(period="max")

    # clickhouse_client = get_clickhouse_client()
    # write_clickhouse(clickhouse_client, symbol, hist)
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
        f'CREATE TABLE IF NOT EXISTS {symbol} (Date Date, Open Float64, High Float64, Low Float64, Close Float64, Volume Int64, Dividends Float64, Stock_Splits Float64) ENGINE = MergeTree() ORDER BY Date PRIMARY KEY Date')

    clickhouse_data = []
    for index, row in data.iterrows():
        year = int(index.strftime('%Y'))
        month = int(index.strftime('%m'))
        day = int(index.strftime('%d'))
        record = [datetime.date(year, month, day), row['Open'], row['High'], row['Low'], row['Close'], int(row['Volume']), row['Dividends'], row['Stock Splits']]
        clickhouse_data.append(record)

    client.insert(symbol, clickhouse_data)


def read_clickhouse(client) -> NoReturn:
    print("Result:", client.query("select * from AAPL where Date == '2024-05-10'").result_set)


def save_to_csv(df_list, symbol):
    df = pd.concat(df_list)
    df.to_csv(f'{symbol}.csv')


if __name__ == "__main__":
    main()
