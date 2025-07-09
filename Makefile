.DEFAULT_GOAL := help
.PHONY: help
help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: demo
demo:
	@uv run main.py --symbol BTCUSDT --start 2020-01-02 --end 2020-01-02 --kline 1m

