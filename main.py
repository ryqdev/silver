import argparse

import yfinance as yf
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description='silver')
    parser.add_argument('--data',
                        type=str,
                        help='download data',
                        default='SPY')

    args = parser.parse_args()
    symbol = args.data

    df_list = []
    data = yf.download(symbol, group_by="Ticker", period='1mo')
    df_list.append(data)

    # Combine all dataframes into a single dataframe
    df = pd.concat(df_list)
    df.to_csv(f'{symbol}.csv')


if __name__ == "__main__":
    main()
