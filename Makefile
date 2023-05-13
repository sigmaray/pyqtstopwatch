SHELL=/bin/bash

.PHONY: timer
timer:
	./.venv/bin/python3 ./timer.pyw

.PHONY: stopwatch
stopwatch:
	./.venv/bin/python3 ./stopwatch.pyw

.PHONY: createvenv
createvenv:
	python3 -m venv .venv

usevenv:
	@echo "You should run << source .venv/bin/activate >>"

.PHONY: pipinstall
pipinstall:
	pip install --upgrade pip
	pip install -r requirements.txt 
