"""
Libretro Core & ROM Utilities
Provides inspection and verification of game cores and registered titles.
"""

from typing import List, Optional
import os


def is_game_installed(game_name: str) -> bool:
    """Checks if a game ROM is registered in stable_retro."""
    try:
        import stable_retro as retro
        available = retro.data.list_games(retro.data.Integrations.ALL)
        return game_name in available or f"{game_name}-v0" in available
    except ImportError:
        return False


def get_core_path(core_name: str = "pcsx_rearmed_libretro.dylib") -> Optional[str]:
    """Finds the path to a downloaded Libretro core."""
    workspace = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    local_path = os.path.join(workspace, "cores", core_name)
    if os.path.exists(local_path):
        return local_path
    system_path = os.path.expanduser(f"~/Library/Application Support/RetroArch/cores/{core_name}")
    if os.path.exists(system_path):
        return system_path
    return None
