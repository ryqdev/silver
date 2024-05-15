import backtrader as bt
from typing import Dict
from test import TestStrategy
from smacross import SmaCross


strategies_mapping: Dict[str, bt.Strategy] = {
    "test": TestStrategy,
    "sma": SmaCross
}


def handle_strategy(stragety: str = None) -> bt.Strategy:
    if stragety is not None:
        return strategies_mapping[stragety]
