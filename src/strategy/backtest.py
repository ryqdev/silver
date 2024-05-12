import argparse
import datetime
import os
import toml

import pandas

import clickhouse_connect
import yfinance as yf
import pandas as pd

from typing import NoReturn, List
from loguru import logger
from src.data.data import get_clickhouse_client, read_clickhouse


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def handle_backtest(strategy: str) -> NoReturn:
    logger.info(f"handle_backtest {strategy}")
    with open("strategies/example.toml", 'r') as f:
        config = toml.load(f)
        symbol = config['strategy']['symbol']
        holding = config['strategy']['holding']
        start_date = config['strategy']['start']
        end_date = config['strategy']['end']

    clickhouse_client = get_clickhouse_client()
    start_price = read_clickhouse(clickhouse_client, symbol, start_date)[0][4]
    end_price = read_clickhouse(clickhouse_client, symbol, end_date)[0][4]
    start_port = float(start_price) * int(holding)
    end_port = float(end_price) * int(holding)
    p_h = (end_port - start_port) / start_port
    if p_h >= 0 :
        logger.info(f"P&H: {bcolors.OKGREEN}{100 * p_h}%")
    else:
        logger.info(f"P&H: {bcolors.FAIL}{100 * p_h}%")

