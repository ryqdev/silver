import backtrader as bt
from loguru import logger

import backtrader_ib_insync as ibnew



def live_trader(symbol: str, strategy_class: bt.Strategy) -> None:
    logger.info(f"Trading: {symbol}, strategy: {strategy_class}")

    cerebro = bt.Cerebro()

    store = ibnew.IBStore(port=7497)

    data = store.getdata(dataname='USD.JPY', sectype='CASH', exchange='IDEALPRO', timeframe=bt.TimeFrame.Seconds)
    # data = store.getdata(dataname='SPY', sectype='STK', exchange='BYX', timeframe=bt.TimeFrame.Seconds)

    cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=1)

    cerebro.broker = store.getbroker()
    cerebro.addstrategy(strategy_class)
    cerebro.run()

