# Setup & Installation Guide

This guide covers setting up **UNO Q Arena** on both host development systems (macOS / Linux Mint / Ubuntu) and the target **Arduino UNO Q** hardware.

## Prerequisites

- **Python**: 3.10, 3.11, or 3.12
- **Git**
- **SDL2 / Pygame** audio and video libraries

## 1. Automated Installation

Clone the repository and run the setup script:

```bash
git clone https://github.com/jvstin47/UNO-Q-Arena-Edge-AI-Retro-Gaming-on-Arduino-UNO-Q.git
cd UNO-Q-Arena-Edge-AI-Retro-Gaming-on-Arduino-UNO-Q
bash scripts/setup.sh
```


## 2. Manual Installation

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Upgrade pip and install package
pip install --upgrade pip
pip install -e ".[dev]"

# 3. Verify environment
python scripts/check_environment.py
```

## 3. Supplying Game ROMs

Because commercial ROMs are copyrighted, place your legally obtained Genesis ROMs into the `roms/` directory:

```bash
# Import and integrate ROMs with Libretro
python scripts/import_roms.py --roms-dir ./roms --integrate
```

## 4. Running the Arena

```bash
# Play against the AI in Street Fighter II
uno-q-arena --game sf2

# Play against the ONNX neural network policy
uno-q-arena --game sf2 --agent onnx

# Run zero-ROM fallback Mock Arena
uno-q-arena --mock

# Run performance benchmark
python scripts/benchmark.py
```
