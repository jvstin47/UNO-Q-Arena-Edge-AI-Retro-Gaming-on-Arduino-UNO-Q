#!/usr/bin/env python3
"""
Automated Latency & FPS Benchmark for UNO Q Arena.
Tests both Heuristic and ONNX policies across 500 frames and produces performance metrics.
"""

import argparse
import subprocess
import sys
import json

def run_benchmark(agent: str, steps: int = 500):
    print(f"\n---> Benchmarking {agent.upper()} Agent ({steps} steps)...")
    cmd = [
        sys.executable, "-m", "uno_q_arena.main",
        "--mock",
        "--headless",
        "--agent", agent,
        "--steps", str(steps),
        "--benchmark"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(f"Error running benchmark: {res.stderr}")

def main():
    parser = argparse.ArgumentParser(description="Run performance benchmarks")
    parser.add_argument("--steps", type=int, default=300, help="Number of frames per agent")
    args = parser.parse_args()

    print("=" * 60)
    print("      UNO Q ARENA SYSTEM BENCHMARK SUITE")
    print("=" * 60)

    run_benchmark("heuristic", steps=args.steps)
    run_benchmark("onnx", steps=args.steps)


if __name__ == "__main__":
    main()
