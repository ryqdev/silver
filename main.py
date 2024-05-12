import argparse
from typing import NoReturn

from src.data.data import handle_data
from src.strategy.backtest import handle_backtest


def main() -> NoReturn:
    parser = argparse.ArgumentParser(description='silver')
    parser.add_argument('--data',
                        type=str,
                        help='fetch data',
                        default=None)
    parser.add_argument('--backtest',
                        type=str,
                        help='backtest strategies',
                        default=None)

    args = parser.parse_args()

    if args.data is not None:
        handle_data(args.data)

    if args.backtest is not None:
        handle_backtest(args.backtest)


if __name__ == "__main__":
    main()
