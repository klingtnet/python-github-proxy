.PHONY: all run test format

all: test

test:
	pytest .

run:
	python -m main

format:
	.venv/bin/black .