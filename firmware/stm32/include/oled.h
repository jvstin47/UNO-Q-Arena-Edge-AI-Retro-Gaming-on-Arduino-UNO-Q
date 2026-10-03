/**
 * @file oled.h
 * @brief SSD1306 128x64 I2C OLED display driver for real-time telemetry HUD.
 */

#ifndef UNO_Q_OLED_H
#define UNO_Q_OLED_H

#include <stdint.h>

void oled_init(void);
void oled_clear(void);
void oled_update_hud(uint8_t p1_hp, uint8_t p2_hp, uint16_t latency_us, uint8_t aggression);

#endif // UNO_Q_OLED_H
