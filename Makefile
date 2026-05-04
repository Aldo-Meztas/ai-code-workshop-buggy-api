PYTHON ?= python3

.PHONY: check-setup install test test-baseline test-extension test-expert test-validation test-pricing test-security run

check-setup:
	$(PYTHON) -c "import sys; print(sys.version.split()[0]); raise SystemExit(0 if sys.version_info >= (3, 10) else 'Python 3.10+ is required')"

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	pytest

test-baseline:
	pytest -m baseline

test-extension:
	pytest -m extension

test-expert:
	pytest -m expert

test-validation:
	pytest tests/test_01_validation.py

test-pricing:
	pytest tests/test_02_pricing.py

test-security:
	pytest tests/test_03_security.py

run:
	uvicorn app.main:app --reload
