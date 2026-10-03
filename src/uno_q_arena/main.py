"""
Main entry point for UNO Q Arena: Edge-AI Retro Gaming on Arduino UNO Q.
"""

import argparse
import sys
import time
import os
from typing import Optional

import pygame

from uno_q_arena.core.config import ArenaConfig
from uno_q_arena.core.input import InputManager, ControllerState
from uno_q_arena.core.telemetry import TelemetryEngine
from uno_q_arena.ai.base import AIAgent
from uno_q_arena.ai.heuristic import StreetFighterHeuristicAgent
from uno_q_arena.ai.racing import RacingHeuristicAgent
from uno_q_arena.ai.onnx_agent import ONNXPolicyAgent
from uno_q_arena.ai.random_agent import RandomAgent
from uno_q_arena.audio.output import AudioManager
from uno_q_arena.emulator.environment import RetroArenaEnvironment
from uno_q_arena.emulator.mock_arena import MockArenaEnvironment
from uno_q_arena.ipc.protocol import BinaryProtocolCodec
from uno_q_arena.ipc.serial_link import SerialIPCLink
from uno_q_arena.ipc.rpmsg_link import RPMsgIPCLink
from uno_q_arena.ui.renderer import DisplayRenderer
from uno_q_arena.ui.hud import HUD


def create_ai_agent(agent_type: str, game_type: str, model_path: Optional[str] = None) -> AIAgent:
    """Instantiate the AI agent based on configuration."""
    if agent_type == "onnx" and model_path and os.path.exists(model_path):
        return ONNXPolicyAgent(model_path)
    elif agent_type == "heuristic":
        if "racing" in game_type.lower():
            return RacingHeuristicAgent()
        return StreetFighterHeuristicAgent()
    elif agent_type == "random":
        return RandomAgent()
    else:
        # Default fallback
        if "racing" in game_type.lower():
            return RacingHeuristicAgent()
        return StreetFighterHeuristicAgent()


def parse_args():
    parser = argparse.ArgumentParser(
        description="UNO Q Arena: Real-Time Human vs AI Retro Gaming on Arduino UNO Q"
    )
    parser.add_argument("--game", "-g", default="sf2", help="Game ID or manifest (e.g. sf2, racing)")
    parser.add_argument("--agent", "-a", default="heuristic", choices=["heuristic", "onnx", "random"], help="AI Agent type")
    parser.add_argument("--model", "-m", default="models/policies/sample_policy.onnx", help="Path to ONNX policy file")
    parser.add_argument("--port", "-p", default=None, help="Serial port for STM32 MCU (e.g. /dev/ttyACM0)")
    parser.add_argument("--rpmsg", action="store_true", help="Use RPMsg IPC endpoint (/dev/rpmsg0)")
    parser.add_argument("--mock", action="store_true", help="Run with mock environment without libretro/ROMs")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode without display")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmark mode and print stats on exit")
    parser.add_argument("--steps", type=int, default=0, help="Max steps to run (0 for infinite)")
    parser.add_argument("--fullscreen", action="store_true", help="Run in fullscreen")
    parser.add_argument("--audio", action="store_true", default=True, help="Enable audio")
    parser.add_argument("--no-audio", dest="audio", action="store_false", help="Disable audio")
    parser.add_argument("--config", "-c", default=None, help="Path to custom config YAML")
    return parser.parse_args()


def main():
    args = parse_args()

    # Load configuration
    config = ArenaConfig.from_yaml(args.config) if args.config else ArenaConfig.load_default()
    if args.game:
        config.game = args.game
    if args.port:
        config.ipc_port = args.port
    if args.rpmsg:
        config.ipc_mode = "rpmsg"
    if args.headless:
        config.headless = True
    config.audio_enabled = args.audio
    config.fullscreen = args.fullscreen

    print("=" * 60)
    print("  UNO Q ARENA: Edge-AI Retro Gaming on Arduino UNO Q")
    print("  Heterogeneous Architecture: Cortex-M33 + QRB2210")
    print("=" * 60)
    print(f"  Game: {config.game} | Agent: {args.agent} | Headless: {config.headless}")
    print(f"  IPC Mode: {config.ipc_mode} | Port: {config.ipc_port or 'Mock/Auto'}")
    print("=" * 60)

    # Initialize Telemetry
    telemetry = TelemetryEngine()

    # Initialize Hardware / IPC Link
    ipc_link = None
    if config.ipc_mode == "rpmsg":
        ipc_link = RPMsgIPCLink()
        ipc_link.connect()
    elif config.ipc_port:
        ipc_link = SerialIPCLink(port=config.ipc_port)
        ipc_link.connect()

    # Initialize Input Manager
    input_mgr = InputManager()

    # Initialize AI Agent
    ai_agent = create_ai_agent(args.agent, config.game, args.model)
    print(f"[AI] Initialized {ai_agent.name} for {config.game}")

    # Initialize Environment
    if args.mock:
        env = MockArenaEnvironment(game_type=config.game)
    else:
        try:
            env = RetroArenaEnvironment(game_type=config.game)
        except Exception as e:
            print(f"[WARNING] Libretro environment initialization failed: {e}")
            print("[INFO] Falling back to MockArenaEnvironment for simulation.")
            env = MockArenaEnvironment(game_type=config.game)

    obs, info = env.reset()

    # Initialize Audio
    audio_mgr = AudioManager(enabled=config.audio_enabled)
    audio_mgr.start()

    # Initialize Renderer & HUD
    renderer = None
    hud = None
    if not config.headless:
        renderer = DisplayRenderer(
            width=config.display_width,
            height=config.display_height,
            fullscreen=config.fullscreen,
            title="UNO Q Arena - Edge-AI Retro Arcade"
        )
        hud = HUD()

    clock = pygame.time.Clock()
    running = True
    show_hud = True
    step_count = 0

    print("[GAME] Starting main loop at target 60 FPS...")

    try:
        while running:
            loop_start = time.perf_counter()

            # 1. Process Pygame Window Events
            if renderer:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        elif event.key == pygame.K_h:
                            show_hud = not show_hud
                        elif event.key == pygame.K_m:
                            audio_mgr.toggle_mute()
                        elif event.key == pygame.K_r:
                            obs, info = env.reset()

            # 2. Poll Input (Keyboard + Hardware IPC)
            keys = pygame.key.get_pressed() if renderer else {}
            p1_state = input_mgr.poll_keyboard(keys)

            if ipc_link and ipc_link.is_connected:
                packet = ipc_link.read_packet()
                if packet and packet.packet_type == BinaryProtocolCodec.MSG_INPUT:
                    p1_state.merge(packet.controller)
                    ai_agent.set_difficulty(packet.aggression_pct)
                    telemetry.record_aggression(packet.aggression_pct)

            p1_action = p1_state.to_genesis_action()

            # 3. AI Agent Step (Inference & Telemetry)
            ai_start = time.perf_counter()
            p2_action, ai_info = ai_agent.act(obs, info)
            ai_latency_ms = (time.perf_counter() - ai_start) * 1000.0
            telemetry.record_inference(ai_latency_ms)

            # 4. Step Simulation / Emulator
            obs, reward, terminated, truncated, info = env.step(p1_action, p2_action)

            # 5. Audio Streaming
            if config.audio_enabled:
                audio_samples = env.get_audio_samples()
                if audio_samples is not None and len(audio_samples) > 0:
                    audio_mgr.queue_audio(audio_samples)

            # 6. Haptic Feedback Trigger on Damage
            p1_damaged = info.get("p1_damaged", False)
            p2_damaged = info.get("p2_damaged", False)

            if p1_damaged and ipc_link and ipc_link.is_connected:
                # Send haptic alert to STM32 for human player
                haptic_pkt = BinaryProtocolCodec.encode_haptic(intensity=220, duration_ms=150)
                ipc_link.send_packet(haptic_pkt)

            # 7. Render Display & HUD
            if renderer:
                renderer.render_frame(obs)
                snap = telemetry.snapshot(
                    p1_health=info.get("p1_health", 100),
                    p2_health=info.get("p2_health", 100),
                    ai_action=ai_info.get("action_name", "IDLE")
                )
                hud.render(renderer.screen, snap, show_hud=show_hud)
                renderer.flip()

            # 8. Send MCU Telemetry Packet
            if ipc_link and ipc_link.is_connected and (step_count % 3 == 0):
                telem_pkt = BinaryProtocolCodec.encode_telemetry(
                    p1_health=info.get("p1_health", 100),
                    p2_health=info.get("p2_health", 100),
                    ai_action_id=ai_info.get("action_id", 0),
                    latency_ms=ai_latency_ms,
                    fps=telemetry.current_fps
                )
                ipc_link.send_packet(telem_pkt)

            # 9. Frame Timing & Step Tracking
            step_count += 1
            if args.steps > 0 and step_count >= args.steps:
                print(f"[INFO] Reached requested step limit ({args.steps}). Stopping.")
                running = False

            if terminated or truncated:
                obs, info = env.reset()

            clock.tick(60)
            telemetry.record_frame(time.perf_counter() - loop_start)

    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user.")
    finally:
        print("\n[CLEANUP] Shutting down UNO Q Arena...")
        audio_mgr.stop()
        env.close()
        if ipc_link:
            ipc_link.close()
        if renderer:
            renderer.close()

        if args.benchmark or True:
            summary = telemetry.get_summary()
            print("\n" + "=" * 50)
            print("         UNO Q ARENA PERFORMANCE SUMMARY")
            print("=" * 50)
            print(f" Total Frames:      {summary.get('total_frames', step_count)}")
            print(f" Average FPS:       {summary.get('avg_fps', 0.0):.2f}")
            print(f" P95 Frame Time:    {summary.get('p95_frame_time_ms', 0.0):.2f} ms")
            print(f" Avg Inference:     {summary.get('avg_inference_ms', 0.0):.2f} ms")
            print(f" Max Inference:     {summary.get('max_inference_ms', 0.0):.2f} ms")
            print("=" * 50)


if __name__ == "__main__":
    main()
