import backtrader as bt
from loguru import logger
from src.color import bcolors

Status = [
    'Created', 'Submitted', 'Accepted', 'Partial', 'Completed',
    'Canceled', 'Expired', 'Margin', 'Rejected',
]


class FooBar(bt.Strategy):
    def __init__(self):
        self.data_live = False
        self.log(f"initiating {bcolors.OKGREEN}live strategy...")

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        logger.info('%s, %s' % (dt.isoformat(), txt))

    def notify_data(self, data, status, *args, **kwargs):
        print('*' * 5, 'DATA NOTIF:', data._getstatusname(status), *args)
        if status == data.LIVE:
            self.data_live = True

    def notify_order(self, order):
        print("OrderStatus", Status[order.status])
        if order.status == order.Completed:
            buysell = 'BUY Completed' if order.isbuy() else 'SELL Completed'
            txt = '{} {}@{}'.format(buysell, order.executed.size,
                                    order.executed.price)
            print(txt)

    def next(self):
        txt = []
        #txt.append('{}'.format(len(self)))
        txt.append('{}'.format(self.data.datetime.datetime(0).isoformat()))
        txt.append('{:.6f}'.format(self.data.open[0]))
        txt.append('{:.6f}'.format(self.data.high[0]))
        txt.append('{:.6f}'.format(self.data.low[0]))
        txt.append('{:.6f}'.format(self.data.close[0]))
        txt.append('{:.0f}'.format(self.data.volume[0]))
        print(','.join(txt))

        if not self.data_live:
            return

        if len(self) % 2 == 0:
            print ('ORDER BUY Created')
            self.buy(size = 3000)

        if len(self) % 2 == 1:
            print ('ORDER SELL Created')
            self.sell(size = 3000)

