# make csv symbol=TLT
csv:
	@python main.py --csv ${symbol}

# make backtrader symbol=SPY strategy=hold plot=true
backtrader: csv
	@python main.py --backtrader ${symbol} --strategy ${strategy} --plot ${plot}

live:
	@python main.py --live 1