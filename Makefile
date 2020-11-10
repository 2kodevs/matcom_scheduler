.DEFAULT_GOAL 	:= help

run: ## Start the bot
	@python main.py

install: ## Install the project requirements
	pip install -r requirements.txt

debug: ## Start the bot in debug mode
	@python main.py --debug

view: ## display the Makefile
	@cat Makefile

edit: ## open the Makefile with `code`
	@code Makefile

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

