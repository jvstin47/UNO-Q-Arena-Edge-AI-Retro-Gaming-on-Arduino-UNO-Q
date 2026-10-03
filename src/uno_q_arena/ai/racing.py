"""
Heuristic Racing Agent for Combat Cars
Controls throttle, reactive steering, obstacle recovery, and offensive item deployment.
"""

import time
import random
from typing import Tuple, Dict, Any, Optional
import numpy as np

from uno_q_arena.core.config import BUTTON_TO_INDEX, NUM_BUTTONS_PER_PLAYER
from uno_q_arena.ai.base import BaseAgent


class RacingHeuristicAgent(BaseAgent):
    """Rule-based racing driver with throttle management and wall recovery."""

    def __init__(self):
        super().__init__(name="RacingHeuristicAgent")
        self.frame_count = 0
        self.stuck_counter = 0

        self.turn_direction = 'RIGHT'
        self.turn_duration = 0

    def predict(
        self,
        observation: np.ndarray,
        info: Optional[Dict[str, Any]] = None
    ) -> Tuple[np.ndarray, float]:
        t0 = time.perf_counter()
        self.frame_count += 1
        action = np.zeros(NUM_BUTTONS_PER_PLAYER, dtype=np.int8)

        info = info or {}
        speed = info.get('speed', 50)

        # 1. Continuous Acceleration (Button 'B' on Genesis)
        action[BUTTON_TO_INDEX['B']] = 1

        # 2. Wall / Collision Unstick Maneuver
        if speed == 0 and self.frame_count > 60:
            self.stuck_counter += 1
            if self.stuck_counter > 30:
                action[BUTTON_TO_INDEX['B']] = 0
                action[BUTTON_TO_INDEX['DOWN']] = 1
                action[BUTTON_TO_INDEX['LEFT']] = 1
                if self.stuck_counter > 75:
                    self.stuck_counter = 0
                latency_ms = (time.perf_counter() - t0) * 1000.0
                return action, latency_ms
        else:
            self.stuck_counter = max(0, self.stuck_counter - 1)

        # 3. Steering Decisions
        if self.turn_duration > 0:
            self.turn_duration -= 1
            action[BUTTON_TO_INDEX[self.turn_direction]] = 1
        else:
            if random.random() < 0.12:
                self.turn_direction = random.choice(['LEFT', 'RIGHT'])
                self.turn_duration = random.randint(8, 22)
                action[BUTTON_TO_INDEX[self.turn_direction]] = 1

        # 4. Weapons & Boost (Button 'A')
        if random.random() < 0.04:
            action[BUTTON_TO_INDEX['A']] = 1

        latency_ms = (time.perf_counter() - t0) * 1000.0
        return action, latency_ms
