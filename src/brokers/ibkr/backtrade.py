import os

from typing import NoReturn
from datetime import datetime
from loguru import logger

import backtrader as bt

from src.util.color import bcolors
from src.csv.csv import handle_csv


def handler_backtrader(symbol: str, strategy_class: bt.Strategy, is_plotting: bool) -> NoReturn:
    logger.info(f"handle_backtrader {strategy_class}, is_plotting: {is_plotting}")

    cerebro = bt.Cerebro()

    # strategy
    cerebro.addstrategy(strategy_class)

    # cash
    original_value: float = strategy_class.cash if hasattr(strategy_class, 'cash') else cerebro.broker.getvalue()
    cerebro.broker.setcash(original_value)
    logger.info('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # data
    data_path:str = f'data/{symbol}.csv'
    # if os.path.isfile(data_path) == False:
    #     handle_csv(symbol)
    data0 = bt.feeds.YahooFinanceData(dataname=data_path,
                                      fromdate=datetime(2000, 1, 1),
                                      todate=datetime(2024, 5, 15))
    cerebro.adddata(data0)

    # analyzer
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='Returns')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')

    # run
    results = cerebro.run()

    # result
    final_value = cerebro.broker.getvalue()

    value_color: str = bcolors.OKGREEN if original_value < final_value else bcolors.FAIL
    logger.info(f'Final Portfolio Value: {value_color}%.2f' % final_value)

    # statistics
    strat = results[0]
    sharp_ratio = strat.analyzers.SharpeRatio.get_analysis()['sharperatio']
    rtot = strat.analyzers.Returns.get_analysis()['rtot']
    drawdown = strat.analyzers.DrawDown.get_analysis()['max']['drawdown']
    logger.info(f"{bcolors.WARNING}******** Statistics ********")
    logger.info(f'Sharpe Ratio:{sharp_ratio}')
    logger.info(f'Returns:{rtot}')
    logger.info(f'DrawDown:{drawdown}')
    logger.info(f"{bcolors.WARNING}****************************")

    # plot
    if is_plotting:
        cerebro.plot(iplot=False)
