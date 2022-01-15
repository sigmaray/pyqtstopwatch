SHELL=/bin/bash

timer:
	./.venv/bin/python3 ./timer.pyw

stopwatch:
	./.venv/bin/python3 ./stopwatch.pyw

createvenv:
	python3 -m venv .venv

usevenv:
	@echo "run << source .venv/bin/activate >>"

pipinstall:
	pip install --upgrade pip
	pip install -r requirements.txt 
