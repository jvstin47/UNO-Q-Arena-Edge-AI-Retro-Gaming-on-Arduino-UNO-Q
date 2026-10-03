/**
 * @file input.c
 * @brief Button debouncing and GPIO scanning implementation.
 */

#include "input.h"

// Active low input pins with pull-ups
static uint16_t last_raw_state = 0;
static uint16_t debounced_state = 0;
static uint8_t debounce_counters[12] = {0};

void input_init(void) {
    // Configure GPIO pins as INPUT_PULLUP
    // In production HAL:
    // GPIO_InitTypeDef GPIO_InitStruct = {0};
    // GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    // GPIO_InitStruct.Pull = GPIO_PULLUP;
    // HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
}

uint16_t input_scan_debounced(void) {
    // In hardware: read GPIOB / GPIOC pins
    // For reference simulation:
    return debounced_state;
}
