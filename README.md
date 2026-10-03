# UNO Q Arena

### Real-Time Human vs AI Retro Gaming on Arduino UNO Q

[![CI Test Suite](https://github.com/jvstin47/UNO-Q-Arena-Edge-AI-Retro-Gaming-on-Arduino-UNO-Q/actions/workflows/tests.yml/badge.svg)](https://github.com/jvstin47/UNO-Q-Arena-Edge-AI-Retro-Gaming-on-Arduino-UNO-Q/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![Arduino UNO Q](https://img.shields.io/badge/Hardware-Arduino%20UNO%20Q-00979D.svg)](https://store.arduino.cc/)

A production-grade edge-AI arcade gaming platform designed explicitly around the heterogeneous dual-brain architecture of the **Arduino UNO Q**. 

```text
Human Player (Sanwa Deck)
            ↓
STM32 Cortex-M33 (Nerves) ──── 1,000 Hz GPIO & Haptics
            ↕
    Framed Binary IPC (RPMsg / High-Speed UART)
            ↕
Qualcomm QRB2210 Linux (Brain) ── ONNX Neural Inference & Libretro Core
            ↓
  60 FPS HDMI Display + 44.1 kHz Stereo PCM Audio
```

---

## ✦ System Highlights

| Feature | Implementation | Specifications |
| :--- | :--- | :--- |
| **Dual-Brain Architecture** | Qualcomm QRB2210 + STM32 Cortex-M33 | Linux MPU for AI/emulation; MCU for real-time I/O |
| **Edge AI Inference** | Quantized ONNX & Tactical Combat FSM | **1.05 ms** average inference latency |
| **Game Runtime** | Libretro 2-Player Versus Engines | Deterministic 60 FPS emulation via `stable-retro` |
| **Human Arcade Input** | Hardware GPIO Scanner with Debounce | 1,000 Hz polling rate (sub-1ms jitter-free input) |
| **Physical Difficulty Dial** | Analog Potentiometer via 12-bit ADC | Dynamic AI aggression adjustment in real time |
| **Haptic Feedback** | PWM ERM / Solenoid Gate Driver | Direct vibration pulses triggered by in-game damage |
| **Visual Telemetry** | SSD1306 OLED (I2C) & WS2812B NeoPixels | Real-time health bars and latency monitor |
| **Audio Engine** | Pygame Mixer Stereo Streaming | 44.1 kHz 16-bit stereo PCM audio buffer |
| **Zero-ROM Fallback** | Built-in Mock Combat Arena | Allows testing and simulation with zero external ROMs |

---

## 🏛️ The Dual-Brain Architecture

The Arduino UNO Q pairs a high-performance application processor with a hard real-time microcontroller:

```text
                    UNO Q ARENA
                         │
             ┌───────────┴───────────┐
             │                       │
       LINUX MPU                 STM32 MCU
       "BRAIN"                   "NERVES"
             │                       │
       ┌─────┴─────┐           ┌─────┴─────┐
       │           │           │           │
      AI       Emulator      Inputs     Peripherals
       │           │           │           │
     ONNX      Libretro      GPIO       OLED
                              │         LEDs
                              │         Haptic
                              │         Dial
             └───────────┬───────────────┘
                         │
                       IPC
```

1. **Qualcomm QRB2210 Linux MPU ("The Brain")**: Executes Libretro emulation, ONNX neural inference, HUD compositing, and stereo audio decoding.
2. **STM32 Cortex-M33 MCU ("The Nerves")**: Scans 12 arcade switches at 1,000 Hz, reads the analog aggression dial, drives NeoPixel health meters, updates the OLED telemetry display, and activates haptic feedback.
3. **Framed Binary IPC**: High-speed framed packets with `0xAA55` magic header exchange input states, match telemetry, and haptic triggers with sub-millisecond round-trip latency.

---

## 📂 Repository Structure

```text
uno-q-arena/
├── README.md                 # Flagship landing page & architecture overview
├── LICENSE                   # MIT License
├── CONTRIBUTING.md            # Guidelines for issues, code style, and PRs
├── CHANGELOG.md               # Version release history
├── pyproject.toml            # Modern Python packaging specification
├── Makefile                  # Build, test, format, and run shortcuts
│
├── docs/                     # Comprehensive technical documentation
│   ├── architecture.md       # Dual-brain hardware & software architecture
│   ├── setup.md              # Installation on macOS, Linux Mint, & target hardware
│   ├── hardware.md           # Arcade deck assembly and wiring guide
│   ├── ipc-protocol.md       # Binary packet framing specification
│   ├── ai-agents.md          # Neural policies and heuristic combat FSMs
│   ├── benchmarking.md       # Frame timing, latency, and throughput metrics
│   ├── troubleshooting.md    # Common issues and debug steps
│   └── diagrams/             # Architecture and wiring vector SVGs
│
├── src/uno_q_arena/          # Main Python application package
│   ├── core/                 # Config, input manager, telemetry, game state
│   ├── ai/                   # ONNX agent, heuristic fighters, racing driver
│   ├── emulator/             # Libretro environment and mock combat arena
│   ├── audio/                # 44.1 kHz stereo PCM audio streaming manager
│   ├── ipc/                  # Binary framed protocol, serial & RPMsg links
│   ├── ui/                   # Pygame screen renderer and HUD overlay
│   └── main.py               # Main CLI and 60 FPS runtime loop
│
├── firmware/stm32/           # Real-time C firmware for STM32 Coprocessor
│   ├── config/board.yaml     # Board configuration and pin assignments
│   ├── include/              # C headers (ipc.h, input.h, haptics.h, etc.)
│   └── src/                  # Implementations (super-loop, debouncing, OLED)
│
├── hardware/                 # Physical deck specifications
│   ├── bom/bom.csv           # Bill of materials and cost breakdown
│   ├── wiring/pinout.md      # GPIO pinout and electrical connections
│   └── wiring/wiring-diagram.svg
│
├── models/                   # Neural network weights and metadata
│   ├── policies/             # Pre-trained ONNX policies (sample_policy.onnx)
│   └── metadata/model.json   # Model shapes, opsets, and training metrics
│
├── games/                    # Game manifests and configurations
│   └── manifests/            # sf2.yaml, racing.yaml (RAM offsets, controls)
│
├── scripts/                  # Utilities and automated workflows
│   ├── setup.sh              # One-step environment setup
│   ├── import_roms.py        # Validates and registers user-supplied ROMs
│   ├── benchmark.py          # Latency and FPS test suite
│   ├── deploy_firmware.sh    # Flashes STM32 MCU via arduino-cli
│   └── check_environment.py  # Health-check script for host setup
│
├── tests/                    # Pytest test suite
│   ├── unit/                 # Unit tests (config, input, ai, ipc)
│   └── integration/          # Full game-loop integration tests
│
└── .github/                  # CI/CD workflows and issue templates
```

---

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/jvstin47/UNO-Q-Arena-Edge-AI-Retro-Gaming-on-Arduino-UNO-Q.git
cd UNO-Q-Arena-Edge-AI-Retro-Gaming-on-Arduino-UNO-Q
bash scripts/setup.sh
```


Or install manually:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Launching the Arena

```bash
# Street Fighter II with Heuristic Combat AI
uno-q-arena --game sf2

# Street Fighter II with ONNX Neural Policy
uno-q-arena --game sf2 --agent onnx

# Combat Cars Racing
uno-q-arena --game racing

# Zero-ROM Fallback Mock Arena (Runs out of the box with zero assets!)
uno-q-arena --mock
```

### 3. Keyboard Controls (Player 1 Human)

| Action | Key | Genesis Mapping |
| :--- | :--- | :--- |
| **Move Up / Jump** | `W` | D-Pad Up |
| **Crouch / Block Low** | `S` | D-Pad Down |
| **Move Left / Retreat** | `A` | D-Pad Left |
| **Move Right / Advance** | `D` | D-Pad Right |
| **Light Punch (Jab)** | `J` | Button `X` |
| **Medium Punch (Strong)** | `K` | Button `Y` |
| **Heavy Punch (Fierce)** | `L` | Button `Z` |
| **Light Kick (Short)** | `U` | Button `A` |
| **Medium Kick (Forward)** | `I` | Button `B` (Gas in Racing) |
| **Heavy Kick (Roundhouse)** | `O` | Button `C` (Brake in Racing) |
| **Start / Pause** | `Enter` | Start |
| **HUD Toggle** | `H` | — |
| **Mute Audio** | `M` | — |
| **Reset Match** | `R` | — |
| **Exit** | `ESC` | — |

---

## ⚡ Performance & Benchmarks

Run the automated benchmark across agents:

```bash
python scripts/benchmark.py --steps 500
```

Typical performance on target hardware / development host:

```text
==================================================
         UNO Q ARENA PERFORMANCE SUMMARY
==================================================
 Target Frame Rate:  60.00 FPS (16.67 ms frame budget)
 Average FPS:        60.00 FPS
 Libretro Core:      ~ 8.10 ms
 Pygame Renderer:    ~ 3.40 ms
 ONNX AI Inference:  ~ 1.05 ms  (Quantized MobileNetV3)
 Heuristic AI FSM:   ~ 0.05 ms
 IPC Round-Trip:     ~ 0.42 ms
 Total Frame Time:   ~ 13.02 ms (< 16.67 ms headroom)
==================================================
```

---

## 🕹️ Legal Notice Regarding Commercial ROMs

**No copyrighted ROMs, disc images, or BIOS files are distributed in this repository.**

Users must legally provide their own dumps of retro game cartridges and place them into the `roms/` directory. Strict `.gitignore` rules prevent any accidental commits of game binaries or save states.

To automatically import and register your ROMs:

```bash
python scripts/import_roms.py --roms-dir ./roms --integrate
```

---

## 🛠️ Development & Testing

```bash
# Run test suite
pytest tests/ -v

# Run linting
make lint

# Run type check
make type-check
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
