#!/usr/bin/env bash
# Deploy firmware to Arduino UNO Q STM32 Coprocessor

set -e

PORT="${1:-/dev/ttyACM0}"
FQBN="arduino:zephyr:uno_q"

echo "============================================================"
echo " Flashing STM32 Coprocessor Firmware"
echo " Port: $PORT | Target: $FQBN"
echo "============================================================"

if ! command -v arduino-cli &> /dev/null; then
    echo "Notice: arduino-cli not found in PATH."
    echo "You can build firmware using STM32CubeIDE or PlatformIO with firmware/stm32/src."
    exit 0
fi

echo "Compiling firmware..."
arduino-cli compile --fqbn "$FQBN" firmware/stm32

echo "Uploading firmware to $PORT..."
arduino-cli upload -p "$PORT" --fqbn "$FQBN" firmware/stm32

echo "Firmware successfully deployed!"
