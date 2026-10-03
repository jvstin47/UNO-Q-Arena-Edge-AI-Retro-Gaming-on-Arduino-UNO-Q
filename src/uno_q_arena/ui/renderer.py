"""
Display Renderer
Manages Pygame window creation, resolution scaling, and surface blitting.
"""

from typing import Tuple
import numpy as np
import pygame


class DisplayRenderer:
    """Handles aspect-preserving retro scaling and surface presentation."""

    def __init__(self, base_size: Tuple[int, int], scale_factor: int = 4, title: str = "UNO Q Arena"):
        self.base_w, self.base_h = base_size
        self.scale_factor = scale_factor
        self.win_w = self.base_w * scale_factor
        self.win_h = self.base_h * scale_factor

        self.screen = pygame.display.set_mode((self.win_w, self.win_h))
        pygame.display.set_caption(title)

    def set_title(self, title: str) -> None:
        pygame.display.set_caption(title)

    def render_frame(self, obs: np.ndarray) -> None:
        """Transposes and scales the observation frame to the window."""
        surf = pygame.surfarray.make_surface(np.transpose(obs, (1, 0, 2)))
        scaled = pygame.transform.scale(surf, (self.win_w, self.win_h))
        self.screen.blit(scaled, (0, 0))

    def flip(self) -> None:
        pygame.display.flip()
