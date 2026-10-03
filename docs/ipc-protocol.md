# Inter-Processor Communication (IPC) Protocol

The communication link between the **Qualcomm Linux MPU** and the **STM32 Cortex-M33 MCU** uses a compact, deterministic binary frame format.

## Framing Format

Every frame begins with a 2-byte magic header (`0xAA55`), followed by a 1-byte packet type ID, a 1-byte payload length, the payload data, and an 8-bit checksum:

```text
+---------------+---------------+---------------+--------------------+---------------+
| MAGIC (2B)    | TYPE (1B)     | LEN (1B)      | PAYLOAD (N Bytes)  | CHECKSUM (1B) |
| 0xAA55        | 0x01..0x03    | 0x00..0xFF    | ...                | Sum(Payload)  |
+---------------+---------------+---------------+--------------------+---------------+
```

## Packet Definitions

### 1. Packet 0x01: Human Input & Aggression Dial (MCU -> MPU)
- **Rate**: 1,000 Hz
- **Payload Length**: 3 bytes
- **Payload Structure**:
  - `uint16_t buttons`: 16-bit bitmask of Sega Genesis controller buttons.
  - `uint8_t aggression`: 0..255 potentiometer reading.
- **Total Frame**: 8 bytes.

### 2. Packet 0x02: Match Telemetry (MPU -> MCU)
- **Rate**: 20 Hz (every 3 frames)
- **Payload Length**: 5 bytes
- **Payload Structure**:
  - `uint8_t p1_health`: 0..100 Player 1 HP.
  - `uint8_t p2_health`: 0..100 Player 2 (AI) HP.
  - `uint16_t latency_us`: AI inference latency in microseconds.
  - `uint8_t action_id`: Active AI action index.
- **Total Frame**: 10 bytes.

### 3. Packet 0x03: Haptic Feedback Trigger (MPU -> MCU)
- **Rate**: Event-driven (triggered on hit detection)
- **Payload Length**: 3 bytes
- **Payload Structure**:
  - `uint8_t severity`: PWM vibration intensity (0..255).
  - `uint16_t duration_ms`: Vibration duration in milliseconds.
- **Total Frame**: 8 bytes.
