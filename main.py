import argparse
import os
from dotenv import load_dotenv

import clickhouse_connect
import yfinance as yf
import pandas as pd


def main():
    # parser = argparse.ArgumentParser(description='silver')
    # parser.add_argument('--data',
    #                     type=str,
    #                     help='download data',
    #                     default='SPY')
    #
    # args = parser.parse_args()
    # symbol = args.data
    #
    # df_list = []
    # data = yf.download(symbol, group_by="Ticker", period='1mo')
    # df_list.append(data)
    #
    # # Combine all dataframes into a single dataframe
    # df = pd.concat(df_list)
    # df.to_csv(f'{symbol}.csv')

    load_dotenv()
    client = clickhouse_connect.get_client(
        host='famep8kcv5.ap-southeast-1.aws.clickhouse.cloud',
        user='default',
        password=os.getenv('CLICKHOUSE_PASSWORD'),
        secure=True
    )
    print("Result:", client.query("select * from TLT where Close < 85").result_set)


if __name__ == "__main__":
    main()

