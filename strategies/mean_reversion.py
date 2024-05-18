import backtrader as bt

from loguru import logger
from src.util.color import bcolors


class MeanReversion(bt.Strategy):
    cash = 1000000
    t = 1

    def __init__(self):
        self.data_ready = False
        self.order = None


    def notify_data(self, data, status):
        print('Data Status =>', data._getstatusname(status))
        if status == data.LIVE:
            self.data_ready = True


    def log(self, txt):
        logger.info(
            f'%s, %s, {bcolors.OKBLUE} %s, %s, %s, {bcolors.WARNING}%s' % (str(self.data.datetime.datetime()), txt, str(self.data.open[0]), str(self.data.high[0]), str(self.data.low[0]), str(self.data.close[0])))

    def next(self):
        if not self.data_ready:
            return
        self.log("data:")
        c_price = self.data.close[0]
        o_price = self.data.open[0]
        if c_price - o_price > 0.1:
            self.log(f"{bcolors.OKGREEN}buy")
            self.order = self.buy(exectype=bt.Order.Market)
        elif c_price - o_price < -0.1:
            self.log(f"{bcolors.FAIL}sell")
            self.order = self.sell(exectype=bt.Order.Market)


    # if self.t == 1:
        #     self.log(f"{bcolors.OKGREEN}buy")
        #     self.order = self.buy(exectype=bt.Order.Market)
        # elif self.t == 0:
        #     self.log(f"{bcolors.FAIL}sell")
        #     self.order = self.sell(exectype=bt.Order.Market)
        # self.t = 1 - self.t

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
