.PHONY: all run test format

all: test

test:
	pytest .

run:
	python -m main --development

format:
	.venv/bin/black .