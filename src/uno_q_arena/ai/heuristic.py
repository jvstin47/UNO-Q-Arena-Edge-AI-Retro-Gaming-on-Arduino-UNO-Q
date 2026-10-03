"""
Heuristic Combat Agent for Street Fighter II
Executes tactical spacing, defensive blocking, and multi-frame combo buffers.
"""

import time
import random
from typing import Tuple, Dict, Any, Optional
import numpy as np

from uno_q_arena.core.config import BUTTON_TO_INDEX, NUM_BUTTONS_PER_PLAYER
from uno_q_arena.ai.base import BaseAgent


class HeuristicAgent(BaseAgent):
    """
    Intelligent Rule-Based Street Fighter II Combat Agent.
    Supports dynamic aggression scaling (tunable via physical dial).
    """

    def __init__(self, aggression: float = 0.5):
        super().__init__(name="SF2HeuristicAgent")
        self.aggression = aggression
        self.combo_queue: list = []
        self.frame_counter = 0

    def set_aggression(self, value: float) -> None:
        """Sets aggression level from 0.0 (passive) to 1.0 (tournament tryhard)."""
        self.aggression = max(0.0, min(1.0, value))

    def set_difficulty(self, difficulty_pct: int) -> None:
        """Sets aggression level from difficulty percentage 0..100."""
        self.set_aggression(difficulty_pct / 100.0)


    def predict(
        self,
        observation: np.ndarray,
        info: Optional[Dict[str, Any]] = None
    ) -> Tuple[np.ndarray, float]:
        t0 = time.perf_counter()
        self.frame_counter += 1
        action = np.zeros(NUM_BUTTONS_PER_PLAYER, dtype=np.int8)

        # 1. Pop from multi-frame combo buffer if executing special move
        if self.combo_queue:
            next_buttons = self.combo_queue.pop(0)
            for btn in next_buttons:
                if btn in BUTTON_TO_INDEX:
                    action[BUTTON_TO_INDEX[btn]] = 1
            latency_ms = (time.perf_counter() - t0) * 1000.0
            return action, latency_ms

        info = info or {}
        p1_x = info.get("p1_x", info.get("enemy_x", 80))
        p2_x = info.get("p2_x", info.get("x", 240))
        dist = abs(p2_x - p1_x)
        facing_left = p2_x > p1_x

        toward = "LEFT" if facing_left else "RIGHT"
        away = "RIGHT" if facing_left else "LEFT"

        # 2. Combat State Machine based on distance & aggression
        fireball_prob = 0.08 + (self.aggression * 0.15)
        attack_prob = 0.40 + (self.aggression * 0.40)

        if dist > 140:
            # Long range: Advance or projectile
            if random.random() < fireball_prob:
                self._queue_fireball(toward)
            else:
                action[BUTTON_TO_INDEX[toward]] = 1

        elif dist > 65:
            # Mid range: Pokes, sweeps, jump-in
            roll = random.random()
            if roll < (1.0 - attack_prob):
                action[BUTTON_TO_INDEX[toward]] = 1
            elif roll < 0.65:
                # Medium Kick poke
                action[BUTTON_TO_INDEX['B']] = 1
            elif roll < 0.85:
                # Sweep (Crouch Heavy Kick)
                action[BUTTON_TO_INDEX['DOWN']] = 1
                action[BUTTON_TO_INDEX['C']] = 1
            else:
                # Jump forward
                action[BUTTON_TO_INDEX['UP']] = 1
                action[BUTTON_TO_INDEX[toward]] = 1

        else:
            # Close range: Throw, block, or Shoryuken
            roll = random.random()
            if roll < 0.25:
                # Defensive Block (Hold away)
                action[BUTTON_TO_INDEX[away]] = 1
                if random.random() < 0.5:
                    action[BUTTON_TO_INDEX['DOWN']] = 1
            elif roll < 0.55:
                # Jabs
                action[BUTTON_TO_INDEX['X']] = 1
            elif roll < 0.80 and self.aggression > 0.3:
                # Dragon Punch
                self._queue_uppercut(toward)
            else:
                # Heavy Punch
                action[BUTTON_TO_INDEX['Z']] = 1

        latency_ms = (time.perf_counter() - t0) * 1000.0
        return action, latency_ms

    def _queue_fireball(self, toward: str) -> None:
        """Quarter-circle forward (Down -> Down+Toward -> Toward + Punch)."""
        self.combo_queue.extend([
            ['DOWN'],
            ['DOWN', toward],
            [toward, 'Y'],
            []
        ])

    def _queue_uppercut(self, toward: str) -> None:
        """Z-motion Shoryuken (Toward -> Down -> Down+Toward + Heavy Punch)."""
        self.combo_queue.extend([
            [toward],
            ['DOWN'],
            ['DOWN', toward, 'Z'],
            []
        ])


StreetFighterHeuristicAgent = HeuristicAgent

