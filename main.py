import argparse
from typing import NoReturn

from src.clickhouse.clickhouse import handle_clickhouse
from src.backtest.backtest import handle_backtest
from src.csv.csv import handle_csv
from src.backtrader.backtrader import handler_backtrader


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

    # Reference: https://www.backtrader.com/docu/
    parser.add_argument('--backtrader',
                        type=str,
                        help='backtrader',
                        default=None)

    args = parser.parse_args()

    if args.csv is not None:
        handle_csv(args.csv)

    if args.clickhouse is not None:
        handle_clickhouse(args.clickhouse)

    if args.backtest is not None:
        handle_backtest(args.backtest)

    if args.backtrader is not None:
        handler_backtrader(args.backtrader)


if __name__ == "__main__":
    main()
