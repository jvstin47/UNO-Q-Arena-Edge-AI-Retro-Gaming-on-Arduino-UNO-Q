.PHONY: help install dev run run-racing benchmark test clean check

PYTHON ?= .venv/bin/python
PIP ?= .venv/bin/pip

help:
	@echo "UNO Q Arena - Developer Commands:"
	@echo "  make install        Install production dependencies"
	@echo "  make dev            Install package in editable mode with test dependencies"
	@echo "  make run            Run Street Fighter II (P1 Human vs P2 AI)"
	@echo "  make run-racing     Run Combat Cars (P1 Human vs P2 AI)"
	@echo "  make benchmark      Run headless performance benchmark"
	@echo "  make test           Run unit and integration test suite"
	@echo "  make check          Run pre-flight environment checks"
	@echo "  make clean          Remove build artifacts and cache directories"

install:
	$(PIP) install -r requirements.txt

dev: install
	$(PIP) install -e .

run:
	$(PYTHON) -m uno_q_arena.main --game sf2 --mode versus

run-racing:
	$(PYTHON) -m uno_q_arena.main --game combat_cars

benchmark:
	$(PYTHON) scripts/benchmark.py --game sf2 --steps 1000

test:
	$(PYTHON) -m pytest tests/

check:
	$(PYTHON) scripts/check_environment.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[cod]" -delete
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .coverage
