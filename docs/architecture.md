# System Architecture & Dual-Brain Design

The **UNO Q Arena** platform is built around the heterogeneous multi-core architecture of the **Arduino UNO Q**, partitioning computing responsibilities between an embedded Linux MPU and a deterministic real-time MCU.

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

---

## 1. Qualcomm QRB2210 Linux MPU ("The Brain")

The QRB2210 runs embedded Linux and executes the heavy computational workloads:
- **Libretro Emulation Core**: Runs retro games (e.g. Genesis *Street Fighter II* and *Combat Cars*) at a strict 60 FPS.
- **Edge AI Policy Engine**: Executes neural networks via ONNX Runtime (MobileNetV3 backbone) or deterministic combat heuristics within a 1.05 ms inference budget.
- **PCM Audio Streaming**: Pulls 44.1 kHz 16-bit stereo PCM buffers from the emulator core and streams them cleanly via low-latency hardware channels.
- **HDMI Video Output**: Renders native retro frames scaled 4x (1280x896) with HUD telemetry overlays.

## 2. STM32 Cortex-M33 MCU ("The Nerves")

The STM32 microcontroller guarantees hard real-time latency and hardware determinism:
- **1,000 Hz Input Polling**: Scans 12 arcade microswitches and handles debouncing in hardware registers with zero jitter.
- **Dynamic AI Aggression Dial**: Continuously samples an analog potentiometer over 12-bit ADC and adjusts AI behavior live.
- **Haptic Feedback Driver**: Generates immediate PWM pulses for ERM/LRA vibration actuators or solenoid kickers upon in-game damage.
- **Dedicated Telemetry Display**: Drives an SSD1306 OLED HUD and WS2812B NeoPixel health bars over hardware I2C/SPI DMA.

## 3. Inter-Processor Communication (IPC) Bridge

The two chips communicate over a compact binary protocol with a `0xAA55` magic header via high-speed UART (115,200 baud) or kernel RPMsg character device (`/dev/rpmsg0`), delivering round-trip latency under 0.5 ms.
