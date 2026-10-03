"""
Mock Street Fighter Environment
Interactive 2D physics and render engine that simulates head-to-head combat
with zero external ROM dependencies.
"""

from typing import Tuple, Dict, Any, Optional
import numpy as np


class MockStreetFighterEnv:
    """Zero-ROM fallback 2D combat arena."""

    WIDTH = 320
    HEIGHT = 224

    def __init__(self, game_type: str = "sf2"):
        self.game_type = game_type
        self.reset()


    def reset(self) -> Tuple[np.ndarray, Dict[str, Any]]:
        self.timer = 99.0
        self.p1_hp = 100
        self.p2_hp = 100
        self.p1_x = 80.0
        self.p2_x = 240.0
        self.p1_y = 170.0
        self.p2_y = 170.0
        self.p1_vy = 0.0
        self.p2_vy = 0.0
        self.p1_anim = "idle"
        self.p2_anim = "idle"
        self.p1_anim_timer = 0
        self.p2_anim_timer = 0
        return self.render(), self._get_info()

    def _get_info(self) -> Dict[str, Any]:
        return {
            "p1_health": int(self.p1_hp),
            "p2_health": int(self.p2_hp),
            "p1_x": int(self.p1_x),
            "p2_x": int(self.p2_x),
            "timer": int(self.timer),
            "is_mock": True
        }

    def step(self, action: np.ndarray, p2_action: Optional[np.ndarray] = None) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        if p2_action is not None:
            p1_act = action
            p2_act = p2_action
        elif len(action) >= 24:
            p1_act = action[0:12]
            p2_act = action[12:24]
        else:
            p1_act = action
            p2_act = np.zeros(12, dtype=np.int8)

        self.timer = max(0.0, self.timer - (1.0 / 60.0))


        # P1 Physics
        if self.p1_vy == 0:
            if p1_act[4]:  # UP
                self.p1_vy = -7.5
            if p1_act[6]:  # LEFT
                self.p1_x = max(30.0, self.p1_x - 2.5)
            if p1_act[7]:  # RIGHT
                self.p1_x = min(self.p2_x - 25.0, self.p1_x + 2.5)

            if p1_act[10] or p1_act[9] or p1_act[11]:
                self.p1_anim = "punch"
                self.p1_anim_timer = 8
                if abs(self.p1_x - self.p2_x) < 45 and not p2_act[7]:
                    self.p2_hp = max(0, self.p2_hp - 3)
            elif p1_act[1] or p1_act[0] or p1_act[8]:
                self.p1_anim = "kick"
                self.p1_anim_timer = 10
                if abs(self.p1_x - self.p2_x) < 55 and not p2_act[7]:
                    self.p2_hp = max(0, self.p2_hp - 4)
            elif p1_act[5]:
                self.p1_anim = "crouch"
            else:
                if self.p1_anim_timer <= 0:
                    self.p1_anim = "idle"
        else:
            self.p1_anim = "jump"

        # P1 Gravity
        if self.p1_y < 170.0 or self.p1_vy < 0:
            self.p1_y += self.p1_vy
            self.p1_vy += 0.45
            if self.p1_y >= 170.0:
                self.p1_y = 170.0
                self.p1_vy = 0.0

        if self.p1_anim_timer > 0:
            self.p1_anim_timer -= 1

        # P2 Physics
        if self.p2_vy == 0:
            if p2_act[4]:
                self.p2_vy = -7.5
            if p2_act[6]:
                self.p2_x = max(self.p1_x + 25.0, self.p2_x - 2.5)
            if p2_act[7]:
                self.p2_x = min(290.0, self.p2_x + 2.5)

            if p2_act[10] or p2_act[9] or p2_act[11]:
                self.p2_anim = "punch"
                self.p2_anim_timer = 8
                if abs(self.p2_x - self.p1_x) < 45 and not p1_act[6]:
                    self.p1_hp = max(0, self.p1_hp - 3)
            elif p2_act[1] or p2_act[0] or p2_act[8]:
                self.p2_anim = "kick"
                self.p2_anim_timer = 10
                if abs(self.p2_x - self.p1_x) < 55 and not p1_act[6]:
                    self.p1_hp = max(0, self.p1_hp - 4)
            elif p2_act[5]:
                self.p2_anim = "crouch"
            else:
                if self.p2_anim_timer <= 0:
                    self.p2_anim = "idle"
        else:
            self.p2_anim = "jump"

        # P2 Gravity
        if self.p2_y < 170.0 or self.p2_vy < 0:
            self.p2_y += self.p2_vy
            self.p2_vy += 0.45
            if self.p2_y >= 170.0:
                self.p2_y = 170.0
                self.p2_vy = 0.0

        if self.p2_anim_timer > 0:
            self.p2_anim_timer -= 1

        terminated = bool(self.p1_hp <= 0 or self.p2_hp <= 0 or self.timer <= 0)
        return self.render(), float(self.p2_hp < 100), terminated, False, self._get_info()

    def render(self) -> np.ndarray:
        frame = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)
        frame[0:80, :] = [35, 55, 105]
        frame[80:160, :] = [75, 45, 35]
        frame[160:224, :] = [125, 95, 65]
        frame[160:163, :] = [175, 145, 95]

        # Draw P1 (White Gi)
        p1_x, p1_y = int(self.p1_x), int(self.p1_y)
        h = 24 if self.p1_anim == "crouch" else 40
        top = p1_y - h
        frame[max(0, top):p1_y, max(0, p1_x - 10):min(self.WIDTH, p1_x + 10)] = [240, 240, 240]
        frame[max(0, top - 12):max(0, top), max(0, p1_x - 7):min(self.WIDTH, p1_x + 7)] = [220, 180, 140]
        frame[max(0, top - 10):max(0, top - 8), max(0, p1_x - 9):min(self.WIDTH, p1_x + 7)] = [220, 30, 30]

        # Draw P2 (Red Gi)
        p2_x, p2_y = int(self.p2_x), int(self.p2_y)
        h2 = 24 if self.p2_anim == "crouch" else 40
        top2 = p2_y - h2
        frame[max(0, top2):p2_y, max(0, p2_x - 10):min(self.WIDTH, p2_x + 10)] = [220, 30, 30]
        frame[max(0, top2 - 12):max(0, top2), max(0, p2_x - 7):min(self.WIDTH, p2_x + 7)] = [220, 180, 140]
        frame[max(0, top2 - 14):max(0, top2 - 9), max(0, p2_x - 8):min(self.WIDTH, p2_x + 8)] = [240, 210, 40]

        return frame

    def get_audio_samples(self) -> Optional[np.ndarray]:
        """Return silent or simulated audio block."""
        return None

    def close(self):
        pass


MockArenaEnvironment = MockStreetFighterEnv

