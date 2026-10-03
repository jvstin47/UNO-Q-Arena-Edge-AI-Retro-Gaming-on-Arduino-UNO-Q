/**
 * @file main.c
 * @brief STM32 Cortex-M33 Main Coprocessor Application for Arduino UNO Q.
 * Handles deterministic 1000 Hz input polling, telemetry HUD, haptic pulses, and NeoPixels.
 */

#include <stdint.h>
#include <stdbool.h>

#include "ipc.h"
#include "input.h"
#include "aggression.h"
#include "haptics.h"
#include "neopixel.h"
#include "oled.h"

int main(void) {
    // 1. Hardware Initialization
    input_init();
    aggression_init();
    haptics_init();
    neopixel_init();
    oled_init();
    ipc_init();

    uint32_t loop_count = 0;
    ipc_telemetry_payload_t telem = {0};
    ipc_haptic_payload_t haptic = {0};

    // 2. Deterministic Super-Loop
    while (1) {
        // Fast 1 kHz Input Scanning
        uint16_t buttons = input_scan_debounced();
        uint8_t aggression = aggression_read_dial();

        // Transmit input state to Qualcomm Linux MPU over IPC
        ipc_send_input(buttons, aggression);

        // Update active haptic pulses
        haptics_update();

        // Poll incoming telemetry and haptic commands from MPU
        if (ipc_poll_telemetry(&telem, &haptic)) {
            if (haptic.duration_ms > 0) {
                haptics_trigger(haptic.intensity, haptic.duration_ms);
            }
            neopixel_render_health(telem.p1_health, telem.p2_health);
            oled_update_hud(telem.p1_health, telem.p2_health, telem.latency_us, aggression);
        }

        loop_count++;
        // Delay 1ms (or wait for SysTick timer flag)
    }

    return 0;
}
