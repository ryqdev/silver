import argparse
from typing import NoReturn, Dict

import backtrader as bt

from src.csv.csv import handle_csv
from src.backtrade.backtrade import handler_backtrader
from src.backtrade.livetrader import live_trader

from strategies.smacross import SmaCross
from strategies.hold import BuyAndHold
from strategies.mean_reversion import MeanReversion


strategies_mapping: Dict[str, bt.Strategy] = {
    "sma": SmaCross,
    "hold": BuyAndHold,
    "mean": MeanReversion
}


def main() -> NoReturn:
    parser = argparse.ArgumentParser(description='silver')

    # Reference: https://www.backtrader.com/docu/
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

    if args.live is not None:
        live_trader(args.live, handle_strategy(args.strategy))

    if args.csv is not None:
        handle_csv(args.csv)

    if args.backtrader is not None:
        handler_backtrader(args.backtrader, handle_strategy(args.strategy), handle_plot(args.plot))


def handle_plot(plot: str) -> bool:
    if plot is not None:
        if plot.lower() in ('yes', 'true', 't', 'y', '1'):
            return True

    return False


def handle_strategy(stragety: str = None) -> bt.Strategy:
    if stragety is not None:
        return strategies_mapping[stragety]


if __name__ == "__main__":
    main()

