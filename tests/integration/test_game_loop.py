"""
Integration test for full game loop stepping with Mock Arena and AI agents.
"""

import numpy as np
from uno_q_arena.emulator.mock_arena import MockArenaEnvironment
from uno_q_arena.ai.heuristic import StreetFighterHeuristicAgent
from uno_q_arena.ai.onnx_agent import ONNXPolicyAgent
from uno_q_arena.core.telemetry import TelemetryEngine


def test_mock_game_loop_with_heuristic():
    env = MockArenaEnvironment(game_type="sf2")
    agent = StreetFighterHeuristicAgent()
    telemetry = TelemetryEngine()

    obs, info = env.reset()
    assert obs.shape == (224, 320, 3)

    for _ in range(60):
        # P1 random or no-op
        p1_action = np.zeros(12, dtype=np.int8)
        p2_action, ai_meta = agent.act(obs, info)

        obs, reward, terminated, truncated, info = env.step(p1_action, p2_action)
        telemetry.record_inference(ai_meta["latency_ms"])

        assert obs.shape == (224, 320, 3)
        assert "p1_health" in info
        assert "p2_health" in info

    summary = telemetry.get_summary()
    assert summary["avg_inference_ms"] < 10.0


def test_mock_game_loop_with_onnx():
    env = MockArenaEnvironment(game_type="sf2")
    agent = ONNXPolicyAgent("models/policies/sample_policy.onnx")

    obs, info = env.reset()
    for _ in range(30):
        p1_action = np.zeros(12, dtype=np.int8)
        p2_action, _ = agent.act(obs, info)
        obs, reward, terminated, truncated, info = env.step(p1_action, p2_action)

    assert obs is not None
