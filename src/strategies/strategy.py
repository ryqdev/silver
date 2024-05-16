import backtrader as bt
from typing import Dict

from src.strategies.smacross import SmaCross
from src.strategies.hold import BuyAndHold
from src.strategies.mean_reversion import MeanReversion


strategies_mapping: Dict[str, bt.Strategy] = {
    "sma": SmaCross,
    "hold": BuyAndHold,
    "mean": MeanReversion
}


def handle_strategy(stragety: str = None) -> bt.Strategy:
    if stragety is not None:
        return strategies_mapping[stragety]
