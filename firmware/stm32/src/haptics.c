/**
 * @file haptics.c
 * @brief Haptic feedback driver implementation using TIM PWM or GPIO pulse.
 */

#include "haptics.h"

static uint16_t remaining_ms = 0;
static uint8_t current_intensity = 0;

void haptics_init(void) {
    // Configure TIM PWM channel for ERM motor / Solenoid gate
}

void haptics_trigger(uint8_t intensity, uint16_t duration_ms) {
    current_intensity = intensity;
    remaining_ms = duration_ms;
    // In production HAL:
    // __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, intensity);
}

void haptics_update(void) {
    if (remaining_ms > 0) {
        remaining_ms--;
        if (remaining_ms == 0) {
            current_intensity = 0;
            // __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, 0);
        }
    }
}
