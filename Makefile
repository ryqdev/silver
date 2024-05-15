run:
	@python main.py --data AAPL --backtest example

backtest:
	@python main.py --backtest example


csv:
	@python main.py --csv MSFT