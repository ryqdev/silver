.DEFAULT_GOAL := help
.PHONY: help
help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: csv
csv: ## Download csv data, e.g.: make csv symbol=TLT
	@python main.py --csv ${symbol}

.PHONY: backtrader
backtrader: csv ## Backtest with backtrader, e.g.: make backtrader symbol=SPY strategy=BuyAndHold plot=true
	@python main.py --backtrader ${symbol} --strategy ${strategy} --plot ${plot}

.PHONY: live
live: ## Live trading, e.g.: make live strategy=paper
	@python main.py --live ${strategy}

