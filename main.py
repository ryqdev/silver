import argparse
from typing import NoReturn

import backtrader as bt

from src.csv.csv import handle_csv
from src.brokers.ibkr.backtrade import handler_backtrader
from src.brokers.ibkr.livetrader import live_trader
from strategies.paper_trading_test import PaperTradingTest

from strategies.smacross import SmaCross
from strategies.hold import BuyAndHold

strategies_mapping: dict[str, bt.Strategy] = {
    "sma": SmaCross,
    "hold": BuyAndHold,
    "paper": PaperTradingTest
}


def main() -> NoReturn:
    parser = argparse.ArgumentParser(description='silver')

    # Backtrader: https://www.backtrader.com/docu/
    parser.add_argument('--backtrader',
                        type=str,
                        help='backtrader',
                        default=None)

    parser.add_argument('--csv',
                        type=str,
                        help='fetch data from yahoo finance and save it to local csv file',
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

    if args.live:
        live_trader(args.live, handle_strategy(args.live))

    if args.csv:
        handle_csv(args.csv)

    if args.backtrader:
        handler_backtrader(args.backtrader, handle_strategy(args.strategy), handle_plot(args.plot))


def handle_plot(plot: str | None) -> bool:
    if plot is not None:
        if plot.lower() in ('yes', 'true', 't', 'y', '1'):
            return True

    return False


def handle_strategy(strategy: str = None) -> bt.Strategy:
    return strategies_mapping[strategy]


if __name__ == "__main__":
    main()

