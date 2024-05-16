import backtrader as bt
from loguru import logger
from src.color import bcolors


class FooBar(bt.Strategy):
    def __init__(self):
        self.log(f"initiating {bcolors.OKGREEN}live strategy...")

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        logger.info('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        # buy and hold
        self.log("next")
