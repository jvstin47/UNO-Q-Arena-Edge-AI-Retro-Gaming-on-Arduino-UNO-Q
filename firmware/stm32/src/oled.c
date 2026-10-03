/**
 * @file oled.c
 * @brief SSD1306 128x64 I2C OLED display driver implementation.
 */

#include "oled.h"
#include <stdio.h>

void oled_init(void) {
    // Configure I2C1 for SSD1306 display commands
}

void oled_clear(void) {
    // Fill screen buffer with 0x00
}

void oled_update_hud(uint8_t p1_hp, uint8_t p2_hp, uint16_t latency_us, uint8_t aggression) {
    char buf[32];
    // In production HAL with u8g2 or ssd1306 library:
    // snprintf(buf, sizeof(buf), "P1:%3d | P2:%3d", p1_hp, p2_hp);
    // ssd1306_SetCursor(0, 0);
    // ssd1306_WriteString(buf, Font_7x10, White);
    // snprintf(buf, sizeof(buf), "AI Inf: %4.1fms", latency_us / 1000.0f);
    // ssd1306_SetCursor(0, 16);
    // ssd1306_WriteString(buf, Font_7x10, White);
    // snprintf(buf, sizeof(buf), "Aggression: %3d%%", (aggression * 100) / 255);
    // ssd1306_SetCursor(0, 32);
    // ssd1306_WriteString(buf, Font_7x10, White);
    // ssd1306_UpdateScreen();
}
