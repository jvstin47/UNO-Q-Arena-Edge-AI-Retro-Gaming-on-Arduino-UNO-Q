/**
 * @file ipc.h
 * @brief Binary framed Inter-Processor Communication (IPC) protocol.
 * Defines packet types, structures, and framing headers for STM32 <-> QRB2210.
 */

#ifndef UNO_Q_IPC_H
#define UNO_Q_IPC_H

#include <stdint.h>
#include <stdbool.h>

#define IPC_MAGIC_HEADER        0xAA55
#define IPC_MSG_INPUT           0x01
#define IPC_MSG_TELEMETRY       0x02
#define IPC_MSG_HAPTIC          0x03

#pragma pack(push, 1)

typedef struct {
    uint16_t magic;         // 0xAA55
    uint8_t  type;          // IPC_MSG_*
    uint8_t  length;        // Payload size in bytes
} ipc_header_t;

typedef struct {
    uint16_t buttons;       // 16-bit bitmask (12 Genesis buttons)
    uint8_t  aggression;    // 0..255 (ADC reading from potentiometer)
} ipc_input_payload_t;

typedef struct {
    uint8_t  p1_health;     // 0..100
    uint8_t  p2_health;     // 0..100
    uint16_t latency_us;    // Microseconds
    uint8_t  action_id;     // Active AI action index
} ipc_telemetry_payload_t;

typedef struct {
    uint8_t  intensity;     // 0..255 PWM duty
    uint16_t duration_ms;   // Milliseconds
} ipc_haptic_payload_t;

#pragma pack(pop)

void ipc_init(void);
void ipc_send_input(uint16_t buttons, uint8_t aggression);
bool ipc_poll_telemetry(ipc_telemetry_payload_t *telem, ipc_haptic_payload_t *haptic);

#endif // UNO_Q_IPC_H
