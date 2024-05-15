import backtrader as bt
from typing import Dict

from src.strategies.demo import TestStrategy
from src.strategies.smacross import SmaCross
from src.strategies.hold import BuyAndHold


strategies_mapping: Dict[str, bt.Strategy] = {
    "test": TestStrategy,
    "sma": SmaCross,
    "hold": BuyAndHold
}


def handle_strategy(stragety: str = None) -> bt.Strategy:
    if stragety is not None:
        return strategies_mapping[stragety]
