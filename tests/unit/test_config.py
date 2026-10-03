"""
Unit tests for configuration loading and validation.
"""

import os
from uno_q_arena.core.config import ArenaConfig, GAMES_CATALOG, GENESIS_BUTTONS


def test_default_config():
    config = ArenaConfig.load_default()
    assert config.game == "sf2"
    assert config.target_fps == 60
    assert config.ai_difficulty == 50
    assert config.audio_enabled is True


def test_config_from_yaml(tmp_path):
    yaml_file = tmp_path / "custom.yaml"
    yaml_file.write_text("game: combat_cars\ntarget_fps: 30\nheadless: true\n")

    config = ArenaConfig.from_yaml(str(yaml_file))
    assert config.game == "combat_cars"
    assert config.target_fps == 30
    assert config.headless is True


def test_button_catalog():
    assert len(GENESIS_BUTTONS) == 12
    assert "UP" in GENESIS_BUTTONS
    assert "A" in GENESIS_BUTTONS
    assert "B" in GENESIS_BUTTONS
    assert "START" in GENESIS_BUTTONS
