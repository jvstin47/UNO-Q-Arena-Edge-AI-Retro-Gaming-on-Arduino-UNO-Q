# Arduino UNO Q Pinout & Wiring Specification

This document maps all hardware connections between the arcade deck peripherals and the **Arduino UNO Q**'s STM32 header pins.

## 1. Arcade Button & Joystick Inputs (Active Low with Internal Pull-Ups)

All switches connect between the designated GPIO pin and Ground (`GND`).

| Function | Button Label | Genesis Mapping | STM32 Pin | Arduino Pin | Internal State |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **D-Pad Up** | Joystick Up | `UP` | PB4 | D4 | `INPUT_PULLUP` |
| **D-Pad Down** | Joystick Down | `DOWN` | PB6 | D6 | `INPUT_PULLUP` |
| **D-Pad Left** | Joystick Left | `LEFT` | PB7 | D7 | `INPUT_PULLUP` |
| **D-Pad Right** | Joystick Right | `RIGHT` | PB10 | D10 | `INPUT_PULLUP` |
| **Light Punch** | Top Row 1 | `X` | PB13 | D13 | `INPUT_PULLUP` |
| **Medium Punch** | Top Row 2 | `Y` | PB12 | D12 | `INPUT_PULLUP` |
| **Heavy Punch** | Top Row 3 | `Z` | PB14 | D14 | `INPUT_PULLUP` |
| **Light Kick** | Bottom Row 1 | `A` | PB1 | D1 | `INPUT_PULLUP` |
| **Medium Kick** | Bottom Row 2 | `B` | PB0 | D0 | `INPUT_PULLUP` |
| **Heavy Kick** | Bottom Row 3 | `C` | PB11 | D11 | `INPUT_PULLUP` |
| **Start / Pause** | Small Button 1 | `START` | PB3 | D3 | `INPUT_PULLUP` |
| **Mode / Select** | Small Button 2 | `MODE` | PB2 | D2 | `INPUT_PULLUP` |

## 2. Analog AI Aggression Tuning Dial

| Device Pin | Connection | Note |
| :--- | :--- | :--- |
| Pin 1 (CCW) | `GND` | Ground reference |
| Pin 2 (Wiper)| `PA0` (Arduino A0) | 12-bit ADC input (0..4095) |
| Pin 3 (CW)  | `+3.3V` | Analog reference voltage |

## 3. SSD1306 128x64 I2C OLED Display

| Display Pin | STM32 Pin | Arduino Pin | Note |
| :--- | :--- | :--- | :--- |
| `VCC` | `+3.3V` or `+5V` | `3V3` | Power |
| `GND` | `GND` | `GND` | Ground |
| `SCL` | `PB8` | `SCL` | I2C Clock (400 kHz) |
| `SDA` | `PB9` | `SDA` | I2C Data |

## 4. WS2812B NeoPixel 8-LED Bar

| NeoPixel Pin | STM32 Pin | Arduino Pin | Note |
| :--- | :--- | :--- | :--- |
| `5V / VDD` | `+5V` | `5V` | High current 5V rail |
| `GND` | `GND` | `GND` | Ground |
| `DIN` | `PB5` | `D5` | 800 kHz High-speed signal line |

## 5. Haptic Feedback Motor / Driver

| Driver Pin | STM32 Pin | Arduino Pin | Note |
| :--- | :--- | :--- | :--- |
| Gate / Control | `PA5` | `D9` (PWM) | TIM2 Channel 1 PWM output |
| `VCC` | `+5V` | `5V` | Solenoid / motor rail |
| `GND` | `GND` | `GND` | Shared system ground |
| Flyback Diode | Across Motor (+ to -) | - | Reverse biased 1N4001 |
