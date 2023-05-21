SHELL=/bin/bash

.PHONY: timer
timer:
	python3 ./timer.pyw

.PHONY: stopwatch
stopwatch:
	python3 ./stopwatch.pyw

.PHONY: createvenv
createvenv:
	python3 -m venv .venv
	@echo "Please run << source .venv/bin/activate >> in your terminal"

.PHONY: pipinstall
pipinstall:
	pip install --upgrade pip
	pip install -r requirements.txt 

.PHONY: docker-build
docker-build:
	docker build -t pyqtstopwatch .

.PHONY: docker-run
docker-run:
	docker run -it -p 8080:8080 pyqtstopwatch

.PHONY: docker-build-and-run
docker-build-and-run:
	docker build -t pyqtstopwatch . && docker run -it -p 8080:8080 pyqtstopwatch

.PHONY: pylint
pylint:
	pylint $$(git ls-files '*.py' '*.pyw')

.PHONY: flake8
flake8:
	flake8 $$(git ls-files '*.py' '*.pyw')

.PHONY: linters
linters: pylint flake8
