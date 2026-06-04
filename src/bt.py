from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import datetime
import re
from loguru import logger

# Allow only characters that appear in legitimate symbols, klines and dates.
# This keeps user-supplied values from escaping the data/ directory.
_SYMBOL_RE = re.compile(r'^[A-Za-z0-9]+$')
_KLINE_RE = re.compile(r'^[0-9]+[smhdwM]$')
_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def _validate(value: str, pattern: re.Pattern, name: str) -> str:
    if not pattern.match(value):
        raise ValueError(f'invalid {name}: {value!r}')
    return value

class BasicStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        logger.info(f'{dt.isoformat()} {txt}')

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

def run(symbol: str, start: str, end: str, kline: str) -> None:
    logger.info(f"starting with {symbol}, start: {start}, end: {end}, kline: {kline}")

    # Validate untrusted inputs before they are used to build a file path,
    # otherwise values like "../../etc/passwd" could escape the data/ dir.
    symbol = _validate(symbol, _SYMBOL_RE, 'symbol')
    kline = _validate(kline, _KLINE_RE, 'kline')
    start = _validate(start, _DATE_RE, 'start')
    end = _validate(end, _DATE_RE, 'end')

    cerebro = bt.Cerebro()

    # Create a custom CSV data feed
    class TimestampCSVData(bt.feeds.GenericCSVData):
        def _loadline(self, linetokens):
            # Convert millisecond timestamp to datetime. The source data is in
            # UTC, so parse it as UTC instead of the host's local timezone.
            timestamp_ms = int(linetokens[0])
            dt = datetime.datetime.fromtimestamp(
                timestamp_ms / 1000.0, tz=datetime.timezone.utc
            )
            linetokens[0] = dt.strftime('%Y-%m-%d %H:%M:%S')
            return super()._loadline(linetokens)

    data = TimestampCSVData(
        dataname=f'data/{symbol}-{kline}-{start}.csv',
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        dtformat='%Y-%m-%d %H:%M:%S',
        timeframe=bt.TimeFrame.Minutes,
        compression=1,
    )

    cerebro.adddata(data)
    cerebro.addstrategy(BasicStrategy)

    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)

    logger.info('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    logger.info('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()
