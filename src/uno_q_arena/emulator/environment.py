"""
Retro Environment Wrapper
Manages 2-Player Libretro emulator instances, RAM extraction,
PCM audio capture, and fallback to MockStreetFighterEnv.
"""

import os
from typing import Tuple, Dict, Any, Optional
import numpy as np

from uno_q_arena.core.config import GAMES_CATALOG, DEFAULT_GAME_KEY
from uno_q_arena.emulator.mock_arena import MockStreetFighterEnv


class RetroEnvironmentWrapper:
    """Standardized multi-game Libretro emulator manager."""

    def __init__(
        self,
        game_key: str = DEFAULT_GAME_KEY,
        players: int = 2,
        state_mode: str = "default"
    ):
        self.game_key = game_key
        self.state_mode = state_mode
        self.players = players
        self.env = None
        self.is_mock = False

        if game_key in GAMES_CATALOG:
            self.game_info = GAMES_CATALOG[game_key]
            self.game_name = self.game_info["name"]
            self.genre = self.game_info["genre"]
        else:
            self.game_info = {"name": game_key, "genre": "arcade", "title": f"UNO Q Arena - {game_key}"}
            self.game_name = game_key
            self.genre = "arcade"

        self._init_env()

    def _init_env(self) -> None:
        try:
            import stable_retro as retro
        except ImportError:
            import retro

        available = retro.data.list_games(retro.data.Integrations.ALL)
        candidates = [self.game_name]
        if not self.game_name.endswith("-v0"):
            candidates.append(f"{self.game_name}-v0")

        chosen = next((c for c in candidates if c in available), None)

        if chosen is not None:
            print(f"[Env] Found verified ROM for '{chosen}'. Initializing Genesis core...")
            try:
                retro_state = retro.State.NONE if self.state_mode == "none" else retro.State.DEFAULT
                self.env = retro.make(
                    game=chosen,
                    state=retro_state,
                    players=self.players,
                    render_mode='rgb_array'
                )

                # Custom Versus State Loader
                versus_file = "roms/sf2_versus.state"
                if self.state_mode == "versus" and os.path.exists(versus_file):
                    with open(versus_file, "rb") as f:
                        self.env.em.set_state(f.read())
                    print(f"[Env] Loaded 2-Player Versus Battle state from {versus_file}!")

                print(f"[Env] Libretro core '{chosen}' active with {self.players} players.")
                return
            except Exception as e:
                print(f"[Env] Core load error: {e}. Falling back to Mock Arena.")

        print(f"[Env] ROM for '{self.game_name}' not found. Starting Mock Combat Arena.")
        self.is_mock = True
        self.env = MockStreetFighterEnv()

    def reset(self) -> Tuple[np.ndarray, Dict[str, Any]]:
        res = self.env.reset()
        if isinstance(res, tuple):
            return res[0], res[1] if len(res) > 1 else {}
        return res, {}

    def step(self, action: np.ndarray, p2_action: Optional[np.ndarray] = None) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        if p2_action is not None:
            full_action = np.concatenate([action, p2_action])
        elif len(action) == 24:
            full_action = action
        else:
            full_action = np.zeros(24, dtype=np.int8)
            full_action[:len(action)] = action

        step_res = self.env.step(full_action)
        if len(step_res) == 5:
            obs, rew, term, trunc, info = step_res
        elif len(step_res) == 4:
            obs, rew, term, info = step_res
            trunc = False
        else:
            obs, rew, term, info = step_res[0], step_res[1], step_res[2], {}
            trunc = False
        return obs, rew, term, trunc, info

    def get_audio(self) -> Optional[np.ndarray]:
        """Extracts 44.1 kHz stereo int16 PCM audio samples."""
        if hasattr(self.env, "em") and hasattr(self.env.em, "get_audio"):
            return self.env.em.get_audio()
        return None

    def get_audio_samples(self) -> Optional[np.ndarray]:
        return self.get_audio()


    def save_state(self, filepath: str) -> bool:
        """Saves current emulator state to disk."""
        if hasattr(self.env, "em") and hasattr(self.env.em, "get_state"):
            try:
                with open(filepath, "wb") as f:
                    f.write(self.env.em.get_state())
                print(f"[Env] State saved to {filepath}!")
                return True
            except Exception as e:
                print(f"[Env] Failed to save state: {e}")
        return False

    def load_state(self, filepath: str) -> bool:
        """Loads saved emulator state from disk."""
        if os.path.exists(filepath) and hasattr(self.env, "em") and hasattr(self.env.em, "set_state"):
            try:
                with open(filepath, "rb") as f:
                    self.env.em.set_state(f.read())
                print(f"[Env] State loaded from {filepath}!")
                return True
            except Exception as e:
                print(f"[Env] Failed to load state: {e}")
        return False

    def render(self) -> np.ndarray:
        if hasattr(self.env, "render"):
            return self.env.render()
        return np.zeros((224, 320, 3), dtype=np.uint8)

    def close(self) -> None:
        if self.env is not None:
            self.env.close()


RetroArenaEnvironment = RetroEnvironmentWrapper

