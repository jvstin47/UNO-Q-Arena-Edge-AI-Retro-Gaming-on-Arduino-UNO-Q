#!/usr/bin/env bash
# Setup script for UNO Q Arena environment

set -e

echo "============================================================"
echo " Setting up UNO Q Arena Environment"
echo "============================================================"

# Check Python version
PYTHON_CMD="python3"
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH."
    exit 1
fi

echo "[1/4] Creating virtual environment (.venv)..."
if [ ! -d ".venv" ]; then
    $PYTHON_CMD -m venv .venv
fi

echo "[2/4] Activating virtual environment..."
source .venv/bin/activate

echo "[3/4] Installing dependencies from pyproject.toml..."
pip install --upgrade pip
pip install -e ".[dev]"

echo "[4/4] Verifying environment..."
python scripts/check_environment.py

echo "============================================================"
echo " Setup complete! To play: uno-q-arena --game sf2"
echo "============================================================"
