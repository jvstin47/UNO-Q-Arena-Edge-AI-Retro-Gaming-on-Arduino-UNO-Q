/**
 * @file input.h
 * @brief GPIO button scanning and debounce engine for arcade controls.
 */

#ifndef UNO_Q_INPUT_H
#define UNO_Q_INPUT_H

#include <stdint.h>
#include <stdbool.h>

// Sega Genesis 6-Button Bit Positions
#define BTN_B       (1 << 0)
#define BTN_A       (1 << 1)
#define BTN_MODE    (1 << 2)
#define BTN_START   (1 << 3)
#define BTN_UP      (1 << 4)
#define BTN_DOWN    (1 << 5)
#define BTN_LEFT    (1 << 6)
#define BTN_RIGHT   (1 << 7)
#define BTN_C       (1 << 8)
#define BTN_Y       (1 << 9)
#define BTN_X       (1 << 10)
#define BTN_Z       (1 << 11)

void input_init(void);
uint16_t input_scan_debounced(void);

#endif // UNO_Q_INPUT_H
