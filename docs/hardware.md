# Hardware Assembly & Deck Construction

The **UNO Q Arena** hardware deck integrates professional Japanese arcade controls with real-time feedback peripherals.

![System Architecture](diagrams/system-architecture.svg)

## Bill of Materials Summary

- **Core Processor**: Arduino UNO Q (Qualcomm QRB2210 + STM32 Cortex-M33)
- **Joystick**: Sanwa JLF-TP-8YT 8-way arcade joystick with 5-pin wire harness
- **Pushbuttons**: 6x Sanwa OBSF-30 snap-in buttons (30mm) + 2x Sanwa OBSF-24 utility buttons
- **Display**: SSD1306 0.96-inch 128x64 I2C OLED display (Address: 0x3C)
- **Illumination**: 8-LED WS2812B NeoPixel strip (5V)
- **Dial**: 10k panel-mount linear potentiometer (Aggression tuner)
- **Haptic Actuator**: 1034 coin vibration motor or 5V mini solenoid driven by a 2N2222 / N-channel MOSFET

Refer to [hardware/bom/bom.csv](file:///Users/justin/Public/projects/RetroArch%20trial/hardware/bom/bom.csv) for the full bill of materials with costs and vendor designators.

## Pinout Map

| Pin | Peripheral Function | Electrical Spec |
| :--- | :--- | :--- |
| **PB0–PB14** | 12x Arcade Switches | `INPUT_PULLUP` (Active Low to GND) |
| **PA0 (A0)** | AI Aggression Potentiometer | Analog In 0..3.3V (12-bit ADC) |
| **PB8 / PB9**| SSD1306 OLED HUD | I2C1 (SCL / SDA at 400 kHz) |
| **PB5 (D5)** | WS2812B NeoPixel Bar | 5V DIN (800 kHz SPI/PWM) |
| **PA5 (D9)** | Haptic Vibration Gate | TIM2 Channel 1 PWM |

Refer to [hardware/wiring/pinout.md](file:///Users/justin/Public/projects/RetroArch%20trial/hardware/wiring/pinout.md) for detailed schematics.
