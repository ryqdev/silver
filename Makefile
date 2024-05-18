# make csv symbol=TLT
csv:
	@python main.py --csv ${symbol}

# make backtrader_csv symbol=SPY strategy=hold plot=true
backtrader_csv: csv
	@python main.py --backtrader ${symbol} --strategy ${strategy} --plot ${plot}

backtrader_ibkr:
	@echo "TODO"

live:
	@python main.py --live 1