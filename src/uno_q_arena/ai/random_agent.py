"""
Random Action Baseline Agent
"""

import time
import random
from typing import Tuple, Dict, Any, Optional
import numpy as np

from uno_q_arena.core.config import NUM_BUTTONS_PER_PLAYER
from uno_q_arena.ai.base import BaseAgent


class RandomAgent(BaseAgent):
    """Generates random occasional button inputs for testing."""

    def __init__(self, action_prob: float = 0.3):
        super().__init__(name="RandomAgent")
        self.action_prob = action_prob


    def predict(
        self,
        observation: np.ndarray,
        info: Optional[Dict[str, Any]] = None
    ) -> Tuple[np.ndarray, float]:
        t0 = time.perf_counter()
        action = np.zeros(NUM_BUTTONS_PER_PLAYER, dtype=np.int8)

        if random.random() < self.action_prob:
            presses = random.choice([1, 2])
            for _ in range(presses):
                idx = random.randint(0, NUM_BUTTONS_PER_PLAYER - 1)
                action[idx] = 1

        latency_ms = (time.perf_counter() - t0) * 1000.0
        return action, latency_ms
