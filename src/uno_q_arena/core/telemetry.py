"""
Telemetry and Performance Tracker
Calculates FPS, AI latency distributions, hit detection events, and hardware metrics.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import time
import numpy as np


@dataclass
class TelemetrySnapshot:
    """Snapshot of system telemetry for UI and HUD rendering."""
    fps: float = 60.0
    inference_latency_ms: float = 0.0
    ipc_latency_ms: float = 0.5
    cpu_usage_pct: float = 12.0
    aggression_pct: int = 50
    p1_health: int = 100
    p2_health: int = 100
    ai_action_name: str = "IDLE"


class TelemetryTracker:
    """Tracks latency metrics, hit events, and match telemetry."""

    def __init__(self, window_size: int = 120):
        self.window_size = window_size
        self.latencies: List[float] = []
        self.frame_count = 0
        self.prev_p1_hp: Optional[int] = None
        self.prev_p2_hp: Optional[int] = None
        self.hit_events: List[Dict[str, Any]] = []

    def record_ai_latency(self, latency_ms: float) -> None:
        """Records an AI inference duration."""
        self.latencies.append(latency_ms)
        if len(self.latencies) > self.window_size * 10:
            self.latencies = self.latencies[-self.window_size:]

    def process_frame_state(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detects health drops or impacts to trigger haptic feedback and LED events.
        Returns a dict of event signals.
        """
        self.frame_count += 1
        events = {"p1_hit": False, "p2_hit": False, "damage": 0, "type": "none"}

        p1_hp = info.get("p1_health", info.get("health", 100))
        p2_hp = info.get("p2_health", info.get("enemy_health", 100))

        if self.prev_p1_hp is not None and p1_hp < self.prev_p1_hp:
            damage = self.prev_p1_hp - p1_hp
            events["p1_hit"] = True
            events["damage"] = damage
            events["type"] = "heavy" if damage >= 12 else ("medium" if damage >= 6 else "light")

        if self.prev_p2_hp is not None and p2_hp < self.prev_p2_hp:
            events["p2_hit"] = True

        self.prev_p1_hp = p1_hp
        self.prev_p2_hp = p2_hp
        return events

    def get_summary(self) -> Dict[str, float]:
        """Returns statistical summary of recorded latencies."""
        if not self.latencies:
            return {"avg": 0.0, "p95": 0.0, "max": 0.0}
        arr = np.array(self.latencies)
        return {
            "avg": float(np.mean(arr)),
            "p95": float(np.percentile(arr, 95)),
            "max": float(np.max(arr))
        }


class TelemetryEngine:
    """Real-time telemetry and benchmarking engine for UNO Q Arena."""

    def __init__(self, window_size: int = 120):
        self.tracker = TelemetryTracker(window_size=window_size)
        self.frame_times: List[float] = []
        self.last_inference_ms: float = 0.0
        self.last_ipc_ms: float = 0.5
        self.current_aggression: int = 50
        self.current_fps: float = 60.0
        self._last_fps_calc = time.perf_counter()
        self._frames_since_calc = 0

    def record_inference(self, latency_ms: float):
        self.last_inference_ms = latency_ms
        self.tracker.record_ai_latency(latency_ms)

    def record_aggression(self, agg_pct: int):
        self.current_aggression = agg_pct

    def record_ipc(self, latency_ms: float):
        self.last_ipc_ms = latency_ms

    def record_frame(self, dt_seconds: float):
        self.frame_times.append(dt_seconds * 1000.0)
        self._frames_since_calc += 1
        now = time.perf_counter()
        elapsed = now - self._last_fps_calc
        if elapsed >= 0.5:
            self.current_fps = self._frames_since_calc / elapsed
            self._frames_since_calc = 0
            self._last_fps_calc = now

        if len(self.frame_times) > 1000:
            self.frame_times = self.frame_times[-500:]

    def snapshot(self, p1_health: int, p2_health: int, ai_action: str) -> TelemetrySnapshot:
        return TelemetrySnapshot(
            fps=self.current_fps,
            inference_latency_ms=self.last_inference_ms,
            ipc_latency_ms=self.last_ipc_ms,
            cpu_usage_pct=15.0,  # Approximate nominal QRB2210 load
            aggression_pct=self.current_aggression,
            p1_health=p1_health,
            p2_health=p2_health,
            ai_action_name=ai_action
        )

    def get_summary(self) -> Dict[str, Any]:
        inf_summary = self.tracker.get_summary()
        ft_arr = np.array(self.frame_times) if self.frame_times else np.array([16.6])
        return {
            "total_frames": len(self.frame_times),
            "avg_fps": self.current_fps,
            "avg_frame_time_ms": float(np.mean(ft_arr)),
            "p95_frame_time_ms": float(np.percentile(ft_arr, 95)),
            "avg_inference_ms": inf_summary["avg"],
            "max_inference_ms": inf_summary["max"]
        }
