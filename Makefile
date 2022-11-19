.PHONY: all run test

all: test

test:
	pytest .

run:
	python -m main