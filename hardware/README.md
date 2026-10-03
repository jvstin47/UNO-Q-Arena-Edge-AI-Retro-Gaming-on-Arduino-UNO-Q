# UNO Q Arena - Hardware Subsystem (`hardware/`)

This directory documents the physical arcade hardware, bill of materials, schematics, PCB breakout, 3D printable CAD mounts, and wiring diagrams for the **UNO Q Arena** platform.

## Architecture Overview

The hardware design centers around the **Arduino UNO Q**, leveraging its heterogeneous dual-processor setup:
- **Qualcomm QRB2210 Linux MPU ("Brain")**: Mounts via micro-HDMI to an external 60 Hz monitor and powers stereo audio output.
- **STM32 Cortex-M33 MCU ("Nerves")**: Interfaces directly with physical arcade switches, an analog potentiometer, an I2C OLED display, an 8-LED WS2812B NeoPixel bar, and a haptic vibration actuator.

## Subdirectories

```text
hardware/
├── bom/
│   ├── bom.csv              # Full Bill of Materials with quantities & reference designators
│   └── suppliers.md         # Sourcing recommendations and vendor links
├── wiring/
│   ├── pinout.md            # GPIO pinout table and electrical specifications
│   └── wiring-diagram.svg   # Vector schematic wiring diagram
├── cad/
│   └── README.md            # Enclosure and mounting CAD files (joystick, OLED, Uno Q)
├── pcb/
│   └── README.md            # Custom button breakout PCB and haptic driver circuit
├── schematics/
│   └── README.md            # Hardware circuit schematics and electrical design
└── README.md
```

## Assembly Instructions

1. **Mounting the Arcade Deck**: Mount the Sanwa JLF joystick and OBSF pushbuttons into a 3mm acrylic or MDF enclosure.
2. **Wiring Switches**: Connect one terminal of each microswitch to Ground (`GND`) and the other to its corresponding STM32 GPIO pin (PB0–PB14). Internal pull-ups are enabled in firmware.
3. **Connecting I2C OLED**: Connect `VCC` to 3.3V, `GND` to Ground, `SCL` to PB8, and `SDA` to PB9.
4. **Aggression Potentiometer**: Connect the outer pins to 3.3V and GND, and the wiper to PA0 (Analog In A0).
5. **NeoPixels & Haptics**: Connect the WS2812B DIN to PB5. Connect the gate of the haptic MOSFET driver to PA5 (D9 PWM).
