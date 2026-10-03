# STM32 Coprocessor Firmware (`firmware/stm32/`)

This directory contains the embedded C firmware running on the **STM32 Cortex-M33** microcontroller of the **Arduino UNO Q**.

## Architecture & Responsibilities

The STM32 acts as the **"Nerves"** of the system:
- **1,000 Hz Deterministic Input Polling**: Hardware GPIO scanning with debouncing for arcade push buttons and microswitches (sub-1ms jitter-free input delivery).
- **Physical Difficulty / Aggression Dial**: 12-bit ADC reading with low-pass noise filtering mapped to an 8-bit dynamic difficulty value.
- **Haptic Vibration Actuation**: Low-latency PWM driver for ERM motors, LRA actuators, or solenoid kickers triggered directly by in-game damage events.
- **Visual Telemetry (SSD1306 OLED & NeoPixels)**: Real-time rendering of health meters, AI inference latency, and combo indicators without burdening the Linux MPU.
- **Binary Framed IPC**: High-speed UART / RPMsg framing protocol to synchronize with the Qualcomm QRB2210 Linux MPU.

## Directory Structure

```text
firmware/stm32/
├── config/
│   └── board.yaml       # Pin assignments and peripheral configuration
├── include/
│   ├── aggression.h     # Potentiometer ADC interface
│   ├── haptics.h        # PWM haptic motor driver
│   ├── input.h          # 12-button arcade GPIO scanner
│   ├── ipc.h            # Binary packet framing headers
│   ├── neopixel.h       # WS2812B RGB LED strip interface
│   └── oled.h           # SSD1306 128x64 display driver
├── src/
│   ├── aggression.c
│   ├── haptics.c
│   ├── input.c
│   ├── ipc.c
│   ├── main.c           # Real-time super-loop
│   ├── neopixel.c
│   └── oled.c
└── README.md
```

## Compilation and Flashing

You can compile and deploy the firmware using the STM32CubeIDE toolchain, Arduino CLI, or PlatformIO:

```bash
# Using Arduino CLI with UNO Q board package
arduino-cli compile --fqbn arduino:zephyr:uno_q firmware/stm32
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:zephyr:uno_q firmware/stm32
```
