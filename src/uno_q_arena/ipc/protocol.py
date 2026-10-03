"""
Inter-Processor Communication (IPC) Binary Protocol
Defines compact framed binary packets exchanged between
the Qualcomm Linux MPU and the STM32 Cortex-M33 MCU.
"""

from dataclasses import dataclass
from typing import Tuple, Optional
import struct

from uno_q_arena.core.input import ControllerState

# Protocol Framing Bytes
MAGIC_HEADER = 0xAA55
PACKET_TYPE_INPUT = 0x01      # MCU -> MPU: Buttons (16-bit) + Aggression (8-bit)
PACKET_TYPE_TELEMETRY = 0x02  # MPU -> MCU: P1 HP (8-bit), P2 HP (8-bit), Latency (16-bit us), Action ID (8-bit)
PACKET_TYPE_HAPTIC = 0x03     # MPU -> MCU: Severity (8-bit), Duration (16-bit ms)


@dataclass
class Packet:
    """Parsed IPC frame container."""
    packet_type: int
    controller: ControllerState
    aggression_pct: int = 50


class BinaryProtocolCodec:
    """Framed binary serialization and deserialization codec."""
    MAGIC = MAGIC_HEADER
    MSG_INPUT = PACKET_TYPE_INPUT
    MSG_TELEMETRY = PACKET_TYPE_TELEMETRY
    MSG_HAPTIC = PACKET_TYPE_HAPTIC

    @classmethod
    def encode_telemetry(
        cls,
        p1_health: int,
        p2_health: int,
        ai_action_id: int,
        latency_ms: float = 0.0,
        fps: float = 60.0
    ) -> bytes:
        lat_us = int(latency_ms * 1000)
        return serialize_telemetry_packet(p1_health, p2_health, lat_us, ai_action_id)

    @classmethod
    def encode_haptic(cls, intensity: int = 200, duration_ms: int = 150) -> bytes:
        return serialize_haptic_packet(intensity, duration_ms)

    @classmethod
    def decode(cls, buffer: bytes) -> Optional[Packet]:
        res = deserialize_input_packet(buffer)
        if res is None:
            return None
        buttons, agg_float = res
        agg_pct = int(agg_float * 100.0)
        return Packet(
            packet_type=cls.MSG_INPUT,
            controller=ControllerState(buttons=buttons, aggression_pct=agg_pct),
            aggression_pct=agg_pct
        )


def serialize_telemetry_packet(
    p1_hp: int,
    p2_hp: int,
    latency_us: int,
    predicted_action_id: int
) -> bytes:
    """
    Packs telemetry data into a 10-byte binary frame for the STM32 OLED & LEDs.
    Format: [MAGIC (2B)][TYPE (1B)][LEN (1B)][P1_HP (1B)][P2_HP (1B)][LAT_US (2B)][ACTION_ID (1B)][CHECKSUM (1B)]
    """
    payload = struct.pack(">BBHB", max(0, min(255, p1_hp)), max(0, min(255, p2_hp)), latency_us, predicted_action_id)
    checksum = sum(payload) & 0xFF
    header = struct.pack(">HBB", MAGIC_HEADER, PACKET_TYPE_TELEMETRY, len(payload))
    return header + payload + bytes([checksum])


def serialize_haptic_packet(severity: int, duration_ms: int) -> bytes:
    """Packs haptic trigger command for the STM32 PWM/Solenoid."""
    payload = struct.pack(">BH", severity, duration_ms)
    checksum = sum(payload) & 0xFF
    header = struct.pack(">HBB", MAGIC_HEADER, PACKET_TYPE_HAPTIC, len(payload))
    return header + payload + bytes([checksum])


def deserialize_input_packet(buffer: bytes) -> Optional[Tuple[int, float]]:
    """
    Parses a controller input frame from the STM32 MCU.
    Returns: (buttons_bitmask: int, aggression_dial: float [0.0..1.0])
    """
    if len(buffer) < 8:
        return None

    magic, ptype, plen = struct.unpack_from(">HBB", buffer, 0)
    if magic != MAGIC_HEADER or ptype != PACKET_TYPE_INPUT or plen != 3:
        return None

    buttons, aggression_raw = struct.unpack_from(">HB", buffer, 4)
    expected_checksum = ((buttons >> 8) + (buttons & 0xFF) + aggression_raw) & 0xFF
    received_checksum = buffer[7]

    if expected_checksum != received_checksum:
        return None

    aggression_float = aggression_raw / 255.0
    return buttons, aggression_float
