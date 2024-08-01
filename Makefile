.DEFAULT_GOAL := help
.PHONY: help
help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# make csv symbol=TLT
.PHONY: csv
csv: ## Download csv data
	@python main.py --csv ${symbol}

# make backtrader symbol=SPY strategy=hold plot=true
.PHONY: backtrader
backtrader: csv ## Backtest with backtrader
	@python main.py --backtrader ${symbol} --strategy ${strategy} --plot ${plot}


# make live strategy=paper
.PHONY: live
live: ## Live trading
	@python main.py --live ${strategy}

