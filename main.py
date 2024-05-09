import argparse
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

    client = clickhouse_connect.get_client(
        host='famep8kcv5.ap-southeast-1.aws.clickhouse.cloud',
        user='default',
        password='0mwC5BD~i3hoK',
        secure=True
    )
    print("Result:", client.query("SELECT 1").result_set[0][0])


if __name__ == "__main__":
    main()

