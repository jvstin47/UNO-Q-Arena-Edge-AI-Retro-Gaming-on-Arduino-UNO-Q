/**
 * @file neopixel.c
 * @brief NeoPixel WS2812B bit-banging / SPI DMA implementation.
 */

#include "neopixel.h"

typedef struct {
    uint8_t g;
    uint8_t r;
    uint8_t b;
} rgb_color_t;

static rgb_color_t leds[NUM_LEDS];

void neopixel_init(void) {
    for (int i = 0; i < NUM_LEDS; i++) {
        leds[i].r = 0;
        leds[i].g = 0;
        leds[i].b = 0;
    }
}

void neopixel_set_color(uint8_t index, uint8_t r, uint8_t g, uint8_t b) {
    if (index < NUM_LEDS) {
        leds[index].r = r;
        leds[index].g = g;
        leds[index].b = b;
    }
}

void neopixel_render_health(uint8_t p1_hp, uint8_t p2_hp) {
    // Left 4 LEDs = P1 Health (Green -> Yellow -> Red)
    // Right 4 LEDs = P2 AI Health
    int p1_active = (p1_hp * 4) / 100;
    for (int i = 0; i < 4; i++) {
        if (i < p1_active) {
            neopixel_set_color(i, 0, 200, 0); // Green
        } else {
            neopixel_set_color(i, 50, 0, 0);  // Dark Red
        }
    }

    int p2_active = (p2_hp * 4) / 100;
    for (int i = 0; i < 4; i++) {
        if (i < p2_active) {
            neopixel_set_color(4 + i, 200, 0, 0); // Red
        } else {
            neopixel_set_color(4 + i, 20, 20, 20); // Off/Dim
        }
    }
}

void neopixel_flash_damage(uint8_t r, uint8_t g, uint8_t b) {
    for (int i = 0; i < NUM_LEDS; i++) {
        neopixel_set_color(i, r, g, b);
    }
}
