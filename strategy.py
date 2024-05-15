import backtrader as bt


class SmaCross(bt.SignalStrategy):
    def __init__(self):
        self.cash = 999999
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)
