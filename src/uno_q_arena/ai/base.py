"""
Abstract Base Class for Player 2 AI Agents.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any, Optional
import numpy as np


class AIAgent(ABC):
    """Abstract Base Class for all AI inference policies."""

    def __init__(self, name: str = "AIAgent"):
        self.name = name

    @abstractmethod
    def predict(
        self,
        observation: np.ndarray,
        info: Optional[Dict[str, Any]] = None
    ) -> Tuple[np.ndarray, float]:
        """
        Calculates controller output from game observation and RAM state.

        Args:
            observation: RGB image frame from emulator (H, W, 3).
            info: Dictionary of RAM state variables (HP, timer, positions).

        Returns:
            action: 12-element numpy array [0 or 1] matching Genesis controller layout.
            latency_ms: Inference calculation time in milliseconds.
        """
        pass

    def act(
        self,
        observation: np.ndarray,
        info: Optional[Dict[str, Any]] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Wrapper returning action array and telemetry metadata dictionary.
        """
        action, latency_ms = self.predict(observation, info)
        action_id = int(np.argmax(action)) if np.any(action) else 0
        action_name = "ACTION" if np.any(action) else "IDLE"
        return action, {
            "latency_ms": latency_ms,
            "action_id": action_id,
            "action_name": action_name
        }

    def set_difficulty(self, difficulty_pct: int) -> None:
        """Adjust agent difficulty from 0 to 100."""
        pass


# Backwards compatibility alias
BaseAgent = AIAgent
