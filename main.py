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
    data = yf.download(symbol, group_by="Ticker")
    df = pd.DataFrame(data)
    df.to_csv(f'data/{symbol}.csv')


if __name__ == "__main__":
    main()
