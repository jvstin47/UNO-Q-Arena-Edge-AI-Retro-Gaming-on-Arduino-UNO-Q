# AI Agents & Inference Architectures

**UNO Q Arena** provides modular Player 2 AI opponents engineered for real-time edge execution.

## Supported Agents

| Agent | Module | Description | Typical Latency |
| :--- | :--- | :--- | :--- |
| **SF2 Heuristic** | `uno_q_arena.ai.heuristic` | Spacing, anti-air dragon punches, fireballs, and dynamic aggression scaling | 0.05 ms |
| **Racing Heuristic** | `uno_q_arena.ai.racing` | Cornering, throttle management, obstacle recovery, and weapon usage | 0.04 ms |
| **ONNX Policy** | `uno_q_arena.ai.onnx_agent` | Deep reinforcement learning policy with quantized MobileNet feature extractor | 1.05 ms |
| **Random Baseline** | `uno_q_arena.ai.random_agent` | Baseline sanity checking and fuzzing agent | 0.02 ms |

## Dynamic Aggression Scaling

The physical potentiometer on the arcade deck adjusts the agent's behavior in real time:
- **Low Aggression (0–30%)**: Defensive posture, high blocking frequency, zoning with long-range pokes.
- **Medium Aggression (30–70%)**: Balanced tournament combat, mix-ups, reactive anti-air counters.
- **Maximum Aggression (70–100%)**: Relentless corner pressure, rapid fireball traps, and frame-trap combo strings.
