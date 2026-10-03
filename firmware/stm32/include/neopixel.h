/**
 * @file neopixel.h
 * @brief WS2812B NeoPixel RGB LED strip driver for health and AI combo indicators.
 */

#ifndef UNO_Q_NEOPIXEL_H
#define UNO_Q_NEOPIXEL_H

#include <stdint.h>

#define NUM_LEDS 8

void neopixel_init(void);
void neopixel_set_color(uint8_t index, uint8_t r, uint8_t g, uint8_t b);
void neopixel_render_health(uint8_t p1_hp, uint8_t p2_hp);
void neopixel_flash_damage(uint8_t r, uint8_t g, uint8_t b);

#endif // UNO_Q_NEOPIXEL_H
