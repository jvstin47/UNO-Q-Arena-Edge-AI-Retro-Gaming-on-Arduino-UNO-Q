"""
Unit tests for AI agents (Heuristic, ONNX, Random).
"""

import numpy as np
from uno_q_arena.ai.heuristic import StreetFighterHeuristicAgent
from uno_q_arena.ai.racing import RacingHeuristicAgent
from uno_q_arena.ai.random_agent import RandomAgent
from uno_q_arena.ai.onnx_agent import ONNXPolicyAgent


def test_street_fighter_heuristic_agent():
    agent = StreetFighterHeuristicAgent(aggression=0.7)
    agent.set_difficulty(90)
    assert agent.aggression == 0.9

    obs = np.zeros((224, 320, 3), dtype=np.uint8)
    info = {"p1_health": 100, "p2_health": 100, "p1_x": 80, "p2_x": 200}

    action, meta = agent.act(obs, info)
    assert isinstance(action, np.ndarray)
    assert len(action) == 12
    assert "latency_ms" in meta
    assert meta["latency_ms"] >= 0.0


def test_racing_heuristic_agent():
    agent = RacingHeuristicAgent()
    obs = np.zeros((224, 320, 3), dtype=np.uint8)
    action, meta = agent.act(obs, {"speed": 40})
    assert len(action) == 12
    assert action[0] == 1  # Continuous throttle 'B'


def test_random_agent():
    agent = RandomAgent()
    obs = np.zeros((224, 320, 3), dtype=np.uint8)
    action, meta = agent.act(obs, {})
    assert len(action) == 12


def test_onnx_agent_inference():
    model_path = "models/policies/sample_policy.onnx"
    agent = ONNXPolicyAgent(model_path)
    obs = np.random.randint(0, 255, (224, 320, 3), dtype=np.uint8)
    action, meta = agent.act(obs, {})

    assert len(action) == 12
    assert meta["latency_ms"] < 20.0  # Must be fast
