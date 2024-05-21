import backtrader as bt
from typing import NoReturn
from loguru import logger
from src.util.color import bcolors

import backtrader_ib_insync as ibnew


class MyStrategy(bt.Strategy):

    def __init__(self):
        print("initializing strategy")
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
        print(",".join(ohlcv))

    def next(self):
        # pass invalid data
        if self.data.volume[0] == 0.0 or self.data.open[0] * self.data.high[0] * self.data.low[0] * self.data.close[0] == 0.0:
            # self.log_data(bcolors.WARNING)
            return
        else:
            self.log_data(bcolors.OKGREEN)

        if not self.data_ready:
            return

        if not self.position:
            self.buy(exectype=bt.Order.Market)
        elif self.position:
            self.sell(exectype=bt.Order.Market)


def live_trader(symbol: str, strategy_class: bt.Strategy) -> NoReturn:
    # TODO: use symbol and strategy_class
    logger.info(f"live trading: {symbol}, strategy: {strategy_class}")

    cerebro = bt.Cerebro()

    store = ibnew.IBStore(port=7497)
    data = store.getdata(dataname='USD.JPY', sectype='CASH', exchange='IDEALPRO', timeframe=bt.TimeFrame.Seconds)
    # data = store.getdata(dataname='SPY', sectype='STK', exchange='BYX', timeframe=bt.TimeFrame.Seconds)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=1)

    cerebro.broker = store.getbroker()
    cerebro.addstrategy(MyStrategy)
    cerebro.run()

