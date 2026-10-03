"""
HUD (Heads-Up Display) and telemetry overlay for UNO Q Arena.
Renders real-time metrics, AI action telemetry, latency graphs, and hardware state.
"""

from typing import Tuple, Optional
import pygame
from uno_q_arena.core.telemetry import TelemetrySnapshot


class HUD:
    """Renders telemetry and status overlays on top of the game screen."""

    def __init__(self, font_name: str = "monospace", font_size: int = 14):
        pygame.font.init()
        self.font = pygame.font.SysFont(font_name, font_size, bold=True)
        self.title_font = pygame.font.SysFont(font_name, font_size + 2, bold=True)
        self.small_font = pygame.font.SysFont(font_name, font_size - 2)

        # Colors
        self.COLOR_BG = (20, 24, 33, 200)
        self.COLOR_BORDER = (45, 55, 72)
        self.COLOR_TEXT = (226, 232, 240)
        self.COLOR_ACCENT = (56, 189, 248)  # Sky blue
        self.COLOR_AI = (244, 63, 94)       # Rose red
        self.COLOR_HUMAN = (34, 197, 94)    # Emerald green
        self.COLOR_WARN = (234, 179, 8)     # Amber yellow

    def render(self, surface: pygame.Surface, snapshot: TelemetrySnapshot, show_hud: bool = True):
        """Draw HUD overlay onto the surface."""
        if not show_hud:
            return

        # Top Bar: Performance & Hardware
        self._render_top_bar(surface, snapshot)

        # Left Overlay: Human vs AI Stats
        self._render_combat_stats(surface, snapshot)

        # Bottom Bar: Controls & Status
        self._render_bottom_bar(surface, snapshot)

    def _render_top_bar(self, surface: pygame.Surface, snap: TelemetrySnapshot):
        width = surface.get_width()
        bar_height = 28
        overlay = pygame.Surface((width, bar_height), pygame.SRCALPHA)
        overlay.fill(self.COLOR_BG)

        # Text elements
        fps_color = self.COLOR_HUMAN if snap.fps >= 55 else (self.COLOR_WARN if snap.fps >= 30 else self.COLOR_AI)
        fps_txt = self.font.render(f"FPS: {snap.fps:4.1f}", True, fps_color)
        inf_txt = self.font.render(f"AI Inf: {snap.inference_latency_ms:4.2f}ms", True, self.COLOR_ACCENT)
        ipc_txt = self.font.render(f"IPC: {snap.ipc_latency_ms:4.2f}ms", True, self.COLOR_TEXT)
        cpu_txt = self.font.render(f"CPU: {snap.cpu_usage_pct:4.1f}%", True, self.COLOR_TEXT)
        agg_txt = self.font.render(f"Aggression: {snap.aggression_pct:3d}%", True, self.COLOR_WARN)

        overlay.blit(fps_txt, (12, 6))
        overlay.blit(inf_txt, (120, 6))
        overlay.blit(ipc_txt, (260, 6))
        overlay.blit(cpu_txt, (380, 6))
        overlay.blit(agg_txt, (width - 150, 6))

        pygame.draw.line(overlay, self.COLOR_BORDER, (0, bar_height - 1), (width, bar_height - 1))
        surface.blit(overlay, (0, 0))

    def _render_combat_stats(self, surface: pygame.Surface, snap: TelemetrySnapshot):
        panel_w = 210
        panel_h = 100
        x = 12
        y = 36

        overlay = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        overlay.fill(self.COLOR_BG)
        pygame.draw.rect(overlay, self.COLOR_BORDER, (0, 0, panel_w, panel_h), 1, border_radius=4)

        # Title
        title = self.title_font.render("DUAL-BRAIN TELEMETRY", True, self.COLOR_ACCENT)
        overlay.blit(title, (8, 6))

        # Human health bar
        p1_label = self.small_font.render(f"P1 (Human): {snap.p1_health}", True, self.COLOR_HUMAN)
        overlay.blit(p1_label, (8, 28))
        self._draw_bar(overlay, 90, 31, 105, 8, max(0.0, min(1.0, snap.p1_health / 100.0)), self.COLOR_HUMAN)

        # AI health bar
        p2_label = self.small_font.render(f"P2 (AI):    {snap.p2_health}", True, self.COLOR_AI)
        overlay.blit(p2_label, (8, 48))
        self._draw_bar(overlay, 90, 51, 105, 8, max(0.0, min(1.0, snap.p2_health / 100.0)), self.COLOR_AI)

        # AI Action
        act_text = self.small_font.render(f"Action: {snap.ai_action_name[:16]}", True, self.COLOR_TEXT)
        overlay.blit(act_text, (8, 72))

        surface.blit(overlay, (x, y))

    def _render_bottom_bar(self, surface: pygame.Surface, snap: TelemetrySnapshot):
        width = surface.get_width()
        height = surface.get_height()
        bar_height = 22
        y = height - bar_height

        overlay = pygame.Surface((width, bar_height), pygame.SRCALPHA)
        overlay.fill(self.COLOR_BG)
        pygame.draw.line(overlay, self.COLOR_BORDER, (0, 0), (width, 0))

        help_txt = self.small_font.render("[H] Toggle HUD   [M] Mute   [R] Reset   [ESC] Exit   |   UNO Q: Cortex-M33 + QRB2210", True, (148, 163, 184))
        overlay.blit(help_txt, (12, 4))

        surface.blit(overlay, (0, y))

    def _draw_bar(self, surface: pygame.Surface, x: int, y: int, width: int, height: int, fraction: float, color: Tuple[int, int, int]):
        pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height), border_radius=2)
        fill_w = int(width * fraction)
        if fill_w > 0:
            pygame.draw.rect(surface, color, (x, y, fill_w, height), border_radius=2)
        pygame.draw.rect(surface, self.COLOR_BORDER, (x, y, width, height), 1, border_radius=2)
