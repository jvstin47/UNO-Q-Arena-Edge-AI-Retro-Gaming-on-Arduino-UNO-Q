"""
ONNX Runtime Neural Inference Agent
Optimized for sub-5ms CPU and Apple Silicon CoreML inference.
"""

import os
import time
from typing import Tuple, Dict, Any, Optional
import numpy as np

from uno_q_arena.core.config import NUM_BUTTONS_PER_PLAYER
from uno_q_arena.ai.base import BaseAgent
from uno_q_arena.ai.heuristic import HeuristicAgent


class ONNXAgent(BaseAgent):
    """Executes pre-trained ONNX neural policies."""

    def __init__(self, model_path: str):
        super().__init__(name="ONNXPolicyAgent")
        self.model_path = model_path
        self.session = None

        if not os.path.exists(model_path):
            print(f"[AI] Model file not found at '{model_path}'. Falling back to HeuristicAgent.")
            self.fallback = HeuristicAgent()
            return


        import onnxruntime as ort
        available_providers = ort.get_available_providers()
        preferred = ['CoreMLExecutionProvider', 'CPUExecutionProvider']
        selected = [p for p in preferred if p in available_providers] or ['CPUExecutionProvider']

        self.session = ort.InferenceSession(model_path, providers=selected)
        self.input_name = self.session.get_inputs()[0].name
        self.input_shape = self.session.get_inputs()[0].shape
        self.fallback = None
        print(f"[AI] ONNX Session initialized using {selected}. Input shape: {self.input_shape}")

    def predict(
        self,
        observation: np.ndarray,
        info: Optional[Dict[str, Any]] = None
    ) -> Tuple[np.ndarray, float]:
        if self.session is None:
            return self.fallback.predict(observation, info)

        t0 = time.perf_counter()
        input_data = self._preprocess(observation, self.input_shape)
        outputs = self.session.run(None, {self.input_name: input_data})

        action_logits = outputs[0][0]
        if len(action_logits) == NUM_BUTTONS_PER_PLAYER:
            action = (action_logits > 0.5).astype(np.int8)
        else:
            action = np.zeros(NUM_BUTTONS_PER_PLAYER, dtype=np.int8)

        latency_ms = (time.perf_counter() - t0) * 1000.0
        return action, latency_ms

    def _preprocess(self, obs: np.ndarray, shape: list) -> np.ndarray:
        arr = np.ascontiguousarray(obs, dtype=np.float32) / 255.0
        if len(shape) == 4 and arr.ndim == 3:
            # (H, W, C) -> (1, C, H, W)
            arr = np.transpose(arr, (2, 0, 1))
            arr = np.expand_dims(arr, axis=0)
        return arr


ONNXPolicyAgent = ONNXAgent

