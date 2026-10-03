"""
Game Session Manager
Coordinates game state, round transitions, resets, and match lifecycle.
"""

from typing import Dict, Any


class GameSession:
    """Encapsulates the active game match lifecycle."""

    def __init__(self, game_key: str = "sf2", mode: str = "versus"):
        self.game_key = game_key
        self.mode = mode
        self.is_paused = False
        self.rounds_played = 0
        self.p1_wins = 0
        self.p2_wins = 0

    def toggle_pause(self) -> bool:
        self.is_paused = not self.is_paused
        return self.is_paused

    def record_match_end(self, info: Dict[str, Any]) -> None:
        self.rounds_played += 1
        p1_hp = info.get("p1_health", info.get("health", 0))
        p2_hp = info.get("p2_health", info.get("enemy_health", 0))
        if p1_hp > p2_hp:
            self.p1_wins += 1
        elif p2_hp > p1_hp:
            self.p2_wins += 1
