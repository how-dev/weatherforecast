FLASK_COMMAND = flask run
FLASK_PARAMS = --debugger --reload
PYTEST_CONFIG = -s -v --cov-report  term-missing -p pytest_asyncio

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@egrep '^(.+)\:.*?#+\ *(.+)' ${MAKEFILE_LIST} | column -t -c 2 -s '#'

run: ## To run project locally
	@echo "--> \033[0;32mUping in the port 5000\033[0m"
	${FLASK_COMMAND} ${FLASK_PARAMS}

install: ## To build the environment
	@echo "--> \033[0;32mBuilding the environment\033[0m"
	pip install -r requirements.txt
