import argparse
from typing import NoReturn

from src.clickhouse.clickhouse import handle_clickhouse
from src.strategy.backtest import handle_backtest
from src.csv.csv import handle_csv


def main() -> NoReturn:
    parser = argparse.ArgumentParser(description='silver')
    parser.add_argument('--csv',
                        type=str,
                        help='fetch data from yahoo finance and save it to local csv file',
                        default=None)
    parser.add_argument('--clickhouse',
                        type=str,
                        help='fetch data from yahoo finance and save it to clickhouse',
                        default=None)
    parser.add_argument('--backtest',
                        type=str,
                        help='backtest strategies',
                        default=None)

    args = parser.parse_args()


    if args.csv is not None:
        handle_csv(args.csv)


    if args.clickhouse is not None:
        handle_clickhouse(args.clickhouse)


    if args.backtest is not None:
        handle_backtest(args.backtest)


if __name__ == "__main__":
    main()
