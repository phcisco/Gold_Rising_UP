PY := .venv/bin/python
GOLD := .venv/bin/gold

.PHONY: venv install lint typecheck test check fetch compute render run install-launchd

venv:
	uv venv .venv --python 3.11

install: venv
	uv pip install --python $(PY) -e ".[dev]"

lint:
	.venv/bin/ruff check src tests
	.venv/bin/ruff format --check src tests

typecheck:
	.venv/bin/mypy

test:
	.venv/bin/pytest

check: lint typecheck test

fetch:
	$(GOLD) data fetch

compute:
	$(GOLD) compute run

render:
	$(GOLD) render page

run:
	$(GOLD) run daily

install-launchd:
	bash scripts/install-launchd.sh install
