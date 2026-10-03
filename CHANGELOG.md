# Changelog

All notable changes to the **UNO Q Arena** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-10-03
### Added
- **Production Package Architecture**: Transitioned codebase to the `uno_q_arena` modular Python package.
- **Heterogeneous UNO Q Framework**: Integrated Qualcomm QRB2210 Linux MPU software with STM32 Cortex-M33 real-time firmware.
- **Dual Game Support**: 
  - Street Fighter II': Special Champion Edition (2-Player head-to-head fighting).
  - Combat Cars (2-Player top-down combat racing).
- **Sub-Millisecond Edge-AI**: Pre-compiled INT8/FP32 ONNX neural policy (<0.2ms latency on Apple Silicon CoreML / Linux CPU).
- **Audio Pipeline**: Real-time 44.1 kHz 16-bit stereo PCM streaming via Pygame mixer with hotkey muting.
- **Telemetry HUD**: Live FPS, AI decision latency, and real-time P2 AI button input inspector.
- **STM32 Firmware**: Zero-latency interrupt GPIO input driver, SSD1306 OLED telemetry display, WS2812B NeoPixel underglow, and PWM haptic hit feedback.
- **Hardware Documentation**: Complete Bill of Materials (BOM), Arduino UNO Q pinout mapping, and wiring schematics.
- **Automated Tooling**: Game manifest registry, headless benchmark suite, and checksum-verified ROM importer.
