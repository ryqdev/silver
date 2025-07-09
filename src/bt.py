from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import datetime

class BasicStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}')

        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.dataclose[-1]:
                self.log(f'BUY CREATE, Price: {self.dataclose[0]:.2f}')
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.dataclose[-1]:
                self.log(f'SELL CREATE, Price: {self.dataclose[0]:.2f}')
                self.order = self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Create a custom CSV data feed
    class TimestampCSVData(bt.feeds.GenericCSVData):
        def _loadline(self, linetokens):
            # Convert millisecond timestamp to datetime
            timestamp_ms = int(linetokens[0])
            dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000.0)
            linetokens[0] = dt.strftime('%Y-%m-%d %H:%M:%S')
            return super()._loadline(linetokens)

    data = TimestampCSVData(
        dataname='data/BTCUSDT-1m-2020-01-01.csv',
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        dtformat='%Y-%m-%d %H:%M:%S',
        timeframe=bt.TimeFrame.Minutes,
        compression=1,
        fromdate=datetime.datetime(2020, 1, 1),
        todate=datetime.datetime(2020, 1, 2)
    )

    cerebro.adddata(data)
    cerebro.addstrategy(BasicStrategy)

    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()