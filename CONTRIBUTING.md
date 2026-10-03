# Contributing to UNO Q Arena

We welcome contributions to UNO Q Arena! This document provides guidelines for contributing code, firmware, hardware designs, and game manifests.

---

## Code of Conduct
Please be respectful and collaborative. All contributions should adhere to standard open-source best practices.

---

## Architectural Principles
1. **Heterogeneous Separation**:
   - Heavy compute (AI neural inference, Libretro emulation, video rendering) belongs strictly in the Linux MPU stack (`src/uno_q_arena/`).
   - Hard real-time I/O (microsecond GPIO button interrupts, OLED telemetry, PWM haptics, NeoPixel timing) belongs in the STM32 firmware (`firmware/stm32/`).
   - Communication between the two must strictly follow the defined IPC binary packet protocol (`docs/ipc-protocol.md`).
2. **Legal & Hygiene Guardrail**:
   - **NEVER commit commercial ROM binaries or copyrighted BIOS images.**
   - All game definitions must be declared as open manifests in `games/manifests/`.
   - Users are expected to supply their own legally acquired ROM dumps.

---

## Development Workflow
1. Fork and clone the repository.
2. Create an isolated virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install -e .
   ```
3. Run tests before submitting a Pull Request:
   ```bash
   make test
   make benchmark
   ```
4. Follow standard PEP 8 conventions for Python, and Google C Style for STM32 firmware.
