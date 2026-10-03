"""
Player Input Handler
Captures human controls from Keyboard, USB/Bluetooth Gamepads,
and the Arduino UNO Q / STM32 hardware controller via IPC.
"""

from dataclasses import dataclass
from typing import Optional, Dict
import numpy as np
import pygame

from uno_q_arena.core.config import (
    GENESIS_BUTTONS,
    BUTTON_TO_INDEX,
    NUM_BUTTONS_PER_PLAYER,
    DEFAULT_KEY_MAPPING
)


@dataclass
class ControllerState:
    """Represents raw or merged controller button state."""
    buttons: int = 0
    aggression_pct: int = 50

    def merge(self, other: "ControllerState"):
        """Bitwise OR merge of button states and overwrite aggression."""
        self.buttons |= other.buttons
        if other.aggression_pct is not None:
            self.aggression_pct = other.aggression_pct

    def to_genesis_action(self) -> np.ndarray:
        """Convert bitmask into a 12-element numpy array for the emulator."""
        action = np.zeros(NUM_BUTTONS_PER_PLAYER, dtype=np.int8)
        for i in range(NUM_BUTTONS_PER_PLAYER):
            if (self.buttons >> i) & 1:
                action[i] = 1
        return action


class InputManager:
    """Unified input manager polling keyboard, gamepads, and hardware states."""

    def __init__(self, key_mapping: Optional[Dict[int, str]] = None):
        self.key_mapping = key_mapping or DEFAULT_KEY_MAPPING
        self.handler = HumanInputHandler(self.key_mapping)

    def poll_keyboard(self, keys: Dict[int, bool]) -> ControllerState:
        """Convert pressed keys dictionary into ControllerState bitmask."""
        bitmask = 0
        for key_code, button_name in self.key_mapping.items():
            if keys.get(key_code, False):
                idx = BUTTON_TO_INDEX.get(button_name, -1)
                if idx >= 0:
                    bitmask |= (1 << idx)
        return ControllerState(buttons=bitmask)

    def get_action(self, hw_buttons: Optional[int] = None) -> np.ndarray:
        return self.handler.get_action(hw_buttons)


class HumanInputHandler:

    """Manages Player 1 inputs from Keyboard, Gamepad, or Hardware IPC."""

    def __init__(self, key_mapping: Optional[Dict[int, str]] = None):
        self.key_mapping = key_mapping or DEFAULT_KEY_MAPPING
        self.joystick: Optional[pygame.joystick.Joystick] = None
        self._init_joystick()

    def _init_joystick(self) -> None:
        """Initialize connected joystick if available."""
        if not pygame.joystick.get_init():
            pygame.joystick.init()

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"[Input] Gamepad connected: {self.joystick.get_name()}")
        else:
            print("[Input] No gamepad found. Defaulting to keyboard controls.")

    def get_action(self, hw_buttons: Optional[int] = None) -> np.ndarray:
        """
        Polls current input state and returns a 12-element binary numpy array
        matching the Genesis 6-button controller layout:
        ['B', 'A', 'MODE', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'C', 'Y', 'X', 'Z']

        If hw_buttons bitmask is provided from the STM32 controller, it merges it!
        """
        action = np.zeros(NUM_BUTTONS_PER_PLAYER, dtype=np.int8)

        # 1. Merge STM32 Hardware Bitmask if available
        if hw_buttons is not None:
            for i in range(NUM_BUTTONS_PER_PLAYER):
                if (hw_buttons >> i) & 1:
                    action[i] = 1

        # 2. Poll Keyboard State
        keys = pygame.key.get_pressed()
        for key_code, button_name in self.key_mapping.items():
            if keys[key_code]:
                idx = BUTTON_TO_INDEX[button_name]
                action[idx] = 1

        # 3. Poll Gamepad State
        if self.joystick is not None:
            # D-Pad / Hat
            if self.joystick.get_numhats() > 0:
                hat_x, hat_y = self.joystick.get_hat(0)
                if hat_y == 1:
                    action[BUTTON_TO_INDEX['UP']] = 1
                elif hat_y == -1:
                    action[BUTTON_TO_INDEX['DOWN']] = 1
                if hat_x == -1:
                    action[BUTTON_TO_INDEX['LEFT']] = 1
                elif hat_x == 1:
                    action[BUTTON_TO_INDEX['RIGHT']] = 1

            # Analog Stick fallback
            if self.joystick.get_numaxes() >= 2:
                axis_x = self.joystick.get_axis(0)
                axis_y = self.joystick.get_axis(1)
                deadzone = 0.4
                if axis_y < -deadzone:
                    action[BUTTON_TO_INDEX['UP']] = 1
                elif axis_y > deadzone:
                    action[BUTTON_TO_INDEX['DOWN']] = 1
                if axis_x < -deadzone:
                    action[BUTTON_TO_INDEX['LEFT']] = 1
                elif axis_x > deadzone:
                    action[BUTTON_TO_INDEX['RIGHT']] = 1

            # Gamepad face buttons
            num_buttons = self.joystick.get_numbuttons()
            button_map = {
                0: 'A',     # Light Kick
                1: 'B',     # Medium Kick / Gas
                2: 'X',     # Light Punch
                3: 'Y',     # Medium Punch
                4: 'Z',     # Heavy Punch
                5: 'C',     # Heavy Kick / Brake
                6: 'MODE',  # Mode
                7: 'START', # Start
            }
            for btn_idx, btn_name in button_map.items():
                if btn_idx < num_buttons and self.joystick.get_button(btn_idx):
                    action[BUTTON_TO_INDEX[btn_name]] = 1

        return action
