/**
 * @file ipc.c
 * @brief STM32 IPC implementation over UART/RPMsg.
 */

#include "ipc.h"
#include <string.h>

// Simulated or Hardware UART Tx/Rx buffers
static uint8_t rx_buf[64];
static uint8_t rx_head = 0;

void ipc_init(void) {
    rx_head = 0;
}

void ipc_send_input(uint16_t buttons, uint8_t aggression) {
    uint8_t packet[8];
    packet[0] = (IPC_MAGIC_HEADER >> 8) & 0xFF;
    packet[1] = IPC_MAGIC_HEADER & 0xFF;
    packet[2] = IPC_MSG_INPUT;
    packet[3] = 0x03; // Payload length = 3 bytes
    packet[4] = (buttons >> 8) & 0xFF;
    packet[5] = buttons & 0xFF;
    packet[6] = aggression;
    packet[7] = ((packet[4] + packet[5] + packet[6])) & 0xFF; // Checksum

    // In production firmware, write packet to USART / VCP / RPMsg buffer:
    // HAL_UART_Transmit(&huart1, packet, sizeof(packet), 2);
}

bool ipc_poll_telemetry(ipc_telemetry_payload_t *telem, ipc_haptic_payload_t *haptic) {
    // In production firmware, read bytes from USART DMA circular buffer
    // Parse MAGIC_HEADER, TYPE, LENGTH, PAYLOAD, CHECKSUM
    return false;
}
