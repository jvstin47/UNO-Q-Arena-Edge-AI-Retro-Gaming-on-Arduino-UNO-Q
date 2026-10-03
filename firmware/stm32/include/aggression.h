/**
 * @file aggression.h
 * @brief Analog potentiometer ADC reader for dynamic AI difficulty/aggression tuning.
 */

#ifndef UNO_Q_AGGRESSION_H
#define UNO_Q_AGGRESSION_H

#include <stdint.h>

void aggression_init(void);
uint8_t aggression_read_dial(void);

#endif // UNO_Q_AGGRESSION_H
