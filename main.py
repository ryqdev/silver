import argparse
from typing import NoReturn

# from src.clickhouse.clickhouse import handle_clickhouse
# from src.backtest.backtest import handle_backtest
from src.csv.csv import handle_csv
from src.backtrade.backtrade import handler_backtrader
from src.strategies.strategy import handle_strategy
from src.backtrade.livetrader import live_trader


def main() -> NoReturn:
    parser = argparse.ArgumentParser(description='silver')
    parser.add_argument('--csv',
                        type=str,
                        help='fetch data from yahoo finance and save it to local csv file',
                        default=None)
    # parser.add_argument('--clickhouse',
    #                     type=str,
    #                     help='fetch data from yahoo finance and save it to clickhouse',
    #                     default=None)
    # parser.add_argument('--backtest',
    #                     type=str,
    #                     help='backtest strategies',
    #                     default=None)

    # Reference: https://www.backtrader.com/docu/
    parser.add_argument('--backtrader',
                        type=str,
                        help='backtrader',
                        default=None)

    parser.add_argument('--strategy',
                        type=str,
                        help='backtrader strategy',
                        default=None)

    parser.add_argument('--plot',
                        type=str,
                        help='plot',
                        default=None)

    parser.add_argument('--live',
                        type=str,
                        help='plot',
                        default=None)

    args = parser.parse_args()

    if args.live is not None:
        live_trader()

    if args.csv is not None:
        handle_csv(args.csv)

    if args.clickhouse is not None:
        handle_clickhouse(args.clickhouse)

    if args.backtest is not None:
        handle_backtest(args.backtest)

    if args.backtrader is not None:
        handler_backtrader(args.backtrader, handle_strategy(args.strategy), handle_plot(args.plot))


def handle_plot(plot: str) -> bool:
    if plot is not None:
        if plot.lower() in ('yes', 'true', 't', 'y', '1'):
            return True

    return False


if __name__ == "__main__":
    main()

