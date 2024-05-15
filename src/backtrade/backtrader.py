from typing import NoReturn
from datetime import datetime

import backtrader as bt
from loguru import logger
from src.color import bcolors
from strategy import *


def handler_backtrader(symbol: str) -> NoReturn:
    my_strategy = SmaCross()
    logger.info(f"handle_backtrader {my_strategy}")

    cerebro = bt.Cerebro()
    cerebro.addstrategy(my_strategy)

    data0 = bt.feeds.YahooFinanceData(dataname=f'data/{symbol}.csv',
                                      fromdate=datetime(2011, 1, 1),
                                      todate=datetime(2024, 5, 15))

    cerebro.adddata(data0)
    original_value: float = cerebro.broker.getvalue() if my_strategy.cash is not None else 100000.0
    cerebro.broker.setcash(original_value)
    logger.info('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    final_value = cerebro.broker.getvalue()
    value_color: str = bcolors.OKGREEN if original_value < final_value else bcolors.FAIL
    logger.info(f'Final Portfolio Value: {value_color}%.2f' % final_value)
    cerebro.plot(iplot=False)

