"""
Unit tests for IPC binary framed encoding and decoding.
"""

from uno_q_arena.ipc.protocol import (
    BinaryProtocolCodec,
    MAGIC_HEADER,
    serialize_telemetry_packet,
    serialize_haptic_packet,
    deserialize_input_packet
)


def test_telemetry_packet_serialization():
    pkt = BinaryProtocolCodec.encode_telemetry(
        p1_health=85,
        p2_health=60,
        ai_action_id=4,
        latency_ms=1.25,
        fps=60.0
    )
    assert len(pkt) == 10
    assert pkt[0] == (MAGIC_HEADER >> 8) & 0xFF
    assert pkt[1] == MAGIC_HEADER & 0xFF
    assert pkt[2] == BinaryProtocolCodec.MSG_TELEMETRY


def test_haptic_packet_serialization():
    pkt = BinaryProtocolCodec.encode_haptic(intensity=200, duration_ms=150)
    assert len(pkt) == 8
    assert pkt[2] == BinaryProtocolCodec.MSG_HAPTIC


def test_input_packet_decode():
    # Construct a valid input packet manually
    # Header: AA 55 | Type: 01 | Len: 03 | Payload: Buttons (0x0005) + Aggression (0x80) | Checksum
    buttons = 0x0005
    aggression = 0x80
    checksum = ((buttons >> 8) + (buttons & 0xFF) + aggression) & 0xFF
    raw = bytes([0xAA, 0x55, 0x01, 0x03, 0x00, 0x05, 0x80, checksum])

    packet = BinaryProtocolCodec.decode(raw)
    assert packet is not None
    assert packet.packet_type == BinaryProtocolCodec.MSG_INPUT
    assert packet.controller.buttons == 0x0005
    assert packet.aggression_pct == int((0x80 / 255.0) * 100)
