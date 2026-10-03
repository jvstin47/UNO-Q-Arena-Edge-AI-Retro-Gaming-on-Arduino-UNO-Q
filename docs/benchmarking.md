# Benchmarking & Performance Metrics

Maintaining a rock-solid **60 FPS** (16.6 ms per frame) is critical for retro gaming responsiveness. The total frame budget is partitioned as follows:

```text
+-----------------------------------------------------------+
| Total Frame Budget: 16.67 ms (60.0 FPS)                   |
+---------------------+-------------------+-----------------+
| Libretro Simulation | AI Inference      | Pygame Render   |
| ~ 8.0 ms            | ~ 1.05 ms         | ~ 3.5 ms        |
+---------------------+-------------------+-----------------+
```

## Running Benchmarks

```bash
# Automated benchmark script across agents
python scripts/benchmark.py --steps 500

# Standalone benchmark via CLI
uno-q-arena --mock --headless --agent onnx --steps 1000 --benchmark
```

## Sample Output

```text
==================================================
         UNO Q ARENA PERFORMANCE SUMMARY
==================================================
 Total Frames:      500
 Average FPS:       60.00
 P95 Frame Time:    18.20 ms
 Avg Inference:     1.05 ms
 Max Inference:     1.92 ms
==================================================
```
