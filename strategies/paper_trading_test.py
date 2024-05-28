import backtrader as bt
from loguru import logger
from src.util.color import bcolors

class PaperTradingTest(bt.Strategy):

    def __init__(self):
        print("Initializing strategy")
        self.data_ready = False

    def notify_data(self, data, status):
        print('Data Status =>', data._getstatusname(status))
        if status == data.LIVE:
            self.data_ready = True

    def log_data(self, color: str):
        ohlcv = []
        ohlcv.append(str(color))
        ohlcv.append(str(self.data.datetime.datetime()))
        ohlcv.append(str(self.data.open[0]))
        ohlcv.append(str(self.data.high[0]))
        ohlcv.append(str(self.data.low[0]))
        ohlcv.append(str(self.data.close[0]))
        ohlcv.append(str(self.data.volume[0]))
        logger.info(",".join(ohlcv))

    def next(self):
        if self.data.volume[0] == 0.0 or self.data.open[0] * self.data.high[0] * self.data.low[0] * self.data.close[0] == 0.0:
            return
        else:
            self.log_data(bcolors.OKGREEN)

        if not self.data_ready:
            return

        if not self.position:
            self.buy(exectype=bt.Order.Market)
        elif self.position:
            self.sell(exectype=bt.Order.Market)

