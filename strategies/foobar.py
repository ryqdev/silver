import backtrader as bt
from loguru import logger

Status = [
    'Created', 'Submitted', 'Accepted', 'Partial', 'Completed',
    'Canceled', 'Expired', 'Margin', 'Rejected',
]


class FooBar(bt.Strategy):
    params = {'body': 0.0}

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        logger.info('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.open = self.data.open
        self.close = self.data.close
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted]:
            self.log('Order Submitted')
            return

        if order.status in [order.Accepted]:
            self.log('Order Accepted')
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'Buy Executed at price {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'Sell Executed at price {order.executed.price:.2f}')

        if order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'Trade P&L {trade.pnl:.2f}')

    def next(self):
        self.log('Next')

        if self.order:
            self.log('Open Order Pending')
            return

        if not self.position:
            if self.close > self.open + self.p.body:
                self.order = self.buy(size=100)
        else:
            if self.close < self.open - self.p.body:
                self.order = self.sell(size=100)  # 第59行
