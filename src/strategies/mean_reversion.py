from src.strategies.strategy import *
from loguru import logger
from src.color import bcolors


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
            f'%s, %s, {bcolors.OKBLUE}close_price: {bcolors.WARNING}%s' % (str(self.data.datetime.datetime()), txt, str(self.data.close[0])))

    def next(self):
        if not self.data_ready:
            return
        if self.t == 1:
            self.log(f"{bcolors.OKGREEN}buy")
            self.order = self.buy()
        elif self.t == 0:
            self.log(f"{bcolors.FAIL}sell")
            self.order = self.sell()
        self.t = 1 - self.t

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
