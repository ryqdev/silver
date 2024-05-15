
run:
	@python main.py --data AAPL --backtest example

backtest:
	@python main.py --backtest example

# make csv symbol=TLT
csv:
	@python main.py --csv ${symbol}

# make backtrader symbol=TLT
backtrader: csv
	@python main.py --backtrader ${symbol}