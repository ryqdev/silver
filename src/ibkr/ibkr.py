from ib_insync import *
from loguru import logger


# test the connect with TWS
def ibkr_paper_trading():
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)

    contract = Stock("AAPL", "SMART", "USD")
    order = LimitOrder("BUY", 1, 180)

    trade = ib.placeOrder(contract, order)
    logger.info(trade)