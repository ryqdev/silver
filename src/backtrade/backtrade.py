from typing import NoReturn
from datetime import datetime

from loguru import logger
import backtrader.analyzers as btanalyzers
from src.color import bcolors
from src.strategies.strategy import *


def handler_backtrader(symbol: str, strategy_class: bt.Strategy) -> NoReturn:
    logger.info(f"handle_backtrader {strategy_class}")

    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy_class)

    data0 = bt.feeds.YahooFinanceData(dataname=f'data/{symbol}.csv',
                                      fromdate=datetime(2021, 1, 1),
                                      todate=datetime(2024, 5, 15))

    cerebro.adddata(data0)
    original_value: float = strategy_class.cash if hasattr(strategy_class, 'cash') else cerebro.broker.getvalue()
    cerebro.broker.setcash(original_value)
    logger.info('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
    results = cerebro.run()
    final_value = cerebro.broker.getvalue()
    value_color: str = bcolors.OKGREEN if original_value < final_value else bcolors.FAIL
    logger.info(f'Final Portfolio Value: {value_color}%.2f' % final_value)
    strat = results[0]

    logger.info('Sharpe Ratio:', strat.analyzers.mysharpe.get_analysis())

    # cerebro.plot(iplot=False, start=datetime(2020, 7, 1), end=datetime(2024, 1, 31))

