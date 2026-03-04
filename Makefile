PYTHON ?= python

.PHONY: setup lint test smoke

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .[dev]

lint:
	ruff check src scripts tests
	ruff format --check src scripts tests

test:
	pytest

smoke:
	$(PYTHON) -c "import lakshai"
	$(PYTHON) scripts/laksh.py smoke
