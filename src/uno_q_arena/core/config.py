"""
Central Configuration for UNO Q Arena
Settings for emulation, resolution scaling, controller layouts, and game metadata.
"""

from typing import List, Dict
import pygame

# Window & Display
WINDOW_TITLE = "UNO Q Arena - Dual-Brain Retro Gaming (Arduino UNO Q)"
SCALE_FACTOR = 4       # Native retro resolution multiplier (e.g. 320x224 -> 1280x896)
TARGET_FPS = 60        # 60 FPS standard retro frame rate

# Supported Games Catalog
GAMES_CATALOG: Dict[str, Dict] = {
    "sf2": {
        "id": "sf2",
        "name": "StreetFighterIISpecialChampionEdition-Genesis-v0",
        "title": "UNO Q Arena - Street Fighter II' (P1 Human vs P2 AI)",
        "genre": "fighting",
        "platform": "genesis",
        "controls_hint": "P1: [WASD] Move | [J/K/L] Punches | [U/I/O] Kicks | [Enter] Start | [R] Reset | [ESC] Quit",
        "default_state": "sf2_versus.state",
        "description": "Authentic 6-button Capcom fighting engine with combo interrupts and defensive spacing."
    },
    "combat_cars": {
        "id": "combat_cars",
        "name": "CombatCars-Genesis-v0",
        "title": "UNO Q Arena - Combat Cars Racing (P1 Human vs P2 AI)",
        "genre": "racing",
        "platform": "genesis",
        "controls_hint": "P1: [A/D] Steer | [I] Gas/Accelerate (B) | [U] Fire/Item (A) | [O] Brake (C) | [Enter] Start",
        "default_state": "1Player.Jackyl.Level1",
        "description": "2-Player top-down combat racing with drift handling and defensive weapons."
    }
}
DEFAULT_GAME_KEY = "sf2"

# Sega Genesis 6-Button Controller Action Layout
# Index: 0   1    2       3        4     5       6       7        8    9    10   11
# Name:  B,  A,   MODE,   START,   UP,   DOWN,   LEFT,   RIGHT,   C,   Y,   X,   Z
GENESIS_BUTTONS: List[str] = [
    'B',     # 0: Medium Kick (or Gas in Racing)
    'A',     # 1: Light Kick (or Weapon in Racing)
    'MODE',  # 2: Mode button
    'START', # 3: Start / Pause
    'UP',    # 4: D-Pad Up
    'DOWN',  # 5: D-Pad Down
    'LEFT',  # 6: D-Pad Left
    'RIGHT', # 7: D-Pad Right
    'C',     # 8: Heavy Kick (or Brake in Racing)
    'Y',     # 9: Medium Punch
    'X',     # 10: Light Punch
    'Z'      # 11: Heavy Punch
]

BUTTON_TO_INDEX: Dict[str, int] = {btn: i for i, btn in enumerate(GENESIS_BUTTONS)}
NUM_BUTTONS_PER_PLAYER = len(GENESIS_BUTTONS)  # 12 buttons
TOTAL_ACTION_DIM = NUM_BUTTONS_PER_PLAYER * 2   # 24 buttons (P1: 0..11, P2: 12..23)

# Default Keyboard Mapping for Player 1 (Human)
DEFAULT_KEY_MAPPING: Dict[int, str] = {
    # D-Pad Movement (WASD)
    pygame.K_w: 'UP',
    pygame.K_s: 'DOWN',
    pygame.K_a: 'LEFT',
    pygame.K_d: 'RIGHT',
    
    # Punches (Top Row: J = Light, K = Medium, L = Heavy)
    pygame.K_j: 'X',      # Light Punch
    pygame.K_k: 'Y',      # Medium Punch
    pygame.K_l: 'Z',      # Heavy Punch
    
    # Kicks (Bottom Row: U = Light, I = Medium, O = Heavy)
    pygame.K_u: 'A',      # Light Kick
    pygame.K_i: 'B',      # Medium Kick / Gas
    pygame.K_o: 'C',      # Heavy Kick / Brake
    
    # System Controls
    pygame.K_RETURN: 'START',
    pygame.K_TAB: 'MODE',
}

# UI Overlay Palette
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 230, 110)
COLOR_RED = (235, 55, 55)
COLOR_YELLOW = (255, 215, 0)
COLOR_BLUE = (60, 160, 255)
COLOR_CYAN = (0, 220, 220)
COLOR_BG_OVERLAY = (18, 20, 28, 210)


import os
from dataclasses import dataclass
from typing import Optional
import yaml


@dataclass
class ArenaConfig:
    """Runtime configuration settings for UNO Q Arena."""
    game: str = "sf2"
    ipc_mode: str = "serial"       # "serial", "rpmsg", "mock"
    ipc_port: Optional[str] = None
    headless: bool = False
    fullscreen: bool = False
    display_width: int = 1280
    display_height: int = 896
    target_fps: int = 60
    audio_enabled: bool = True
    ai_agent_type: str = "heuristic"
    ai_model_path: str = "models/policies/sample_policy.onnx"
    ai_difficulty: int = 50

    @classmethod
    def load_default(cls) -> "ArenaConfig":
        """Load default configuration."""
        return cls()

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "ArenaConfig":
        """Load configuration from a YAML file."""
        if not os.path.exists(yaml_path):
            return cls()
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered)

