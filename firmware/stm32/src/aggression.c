/**
 * @file aggression.c
 * @brief Potentiometer reading and smoothing implementation.
 */

#include "aggression.h"

static uint8_t smoothed_val = 128;

void aggression_init(void) {
    // Configure ADC1 Channel for continuous DMA sampling
}

uint8_t aggression_read_dial(void) {
    // Read ADC value (0..4095) and map to 0..255 with low-pass filtering
    // In production HAL:
    // uint32_t raw = HAL_ADC_GetValue(&hadc1);
    // smoothed_val = (smoothed_val * 7 + (raw >> 4)) / 8;
    return smoothed_val;
}
