/**
 * @file haptics.h
 * @brief Haptic feedback driver (PWM rumble motor / ERM / LRA / solenoid trigger).
 */

#ifndef UNO_Q_HAPTICS_H
#define UNO_Q_HAPTICS_H

#include <stdint.h>

void haptics_init(void);
void haptics_trigger(uint8_t intensity, uint16_t duration_ms);
void haptics_update(void);

#endif // UNO_Q_HAPTICS_H
