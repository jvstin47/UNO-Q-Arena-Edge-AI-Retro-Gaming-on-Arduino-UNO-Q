"""
Unit tests for input processing and controller bitmask conversions.
"""

import numpy as np
from uno_q_arena.core.input import ControllerState, InputManager


def test_controller_state_bitmask():
    # Button 0 is 'B', Button 4 is 'UP'
    state = ControllerState(buttons=(1 << 0) | (1 << 4), aggression_pct=75)
    action = state.to_genesis_action()

    assert isinstance(action, np.ndarray)
    assert len(action) == 12
    assert action[0] == 1  # B pressed
    assert action[4] == 1  # UP pressed
    assert action[1] == 0  # A not pressed
    assert state.aggression_pct == 75


def test_controller_state_merge():
    state1 = ControllerState(buttons=(1 << 1), aggression_pct=40)
    state2 = ControllerState(buttons=(1 << 2), aggression_pct=80)
    state1.merge(state2)

    assert state1.buttons == (1 << 1) | (1 << 2)
    assert state1.aggression_pct == 80
