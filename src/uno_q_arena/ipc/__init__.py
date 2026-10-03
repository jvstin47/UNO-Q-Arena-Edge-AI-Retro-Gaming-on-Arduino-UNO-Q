"""Inter-Processor Communication (IPC) interfaces."""

from uno_q_arena.ipc.protocol import (
    serialize_telemetry_packet,
    serialize_haptic_packet,
    deserialize_input_packet
)
from uno_q_arena.ipc.serial_link import SerialIPCLink
from uno_q_arena.ipc.rpmsg_link import RPMsgIPCLink

__all__ = [
    "serialize_telemetry_packet",
    "serialize_haptic_packet",
    "deserialize_input_packet",
    "SerialIPCLink",
    "RPMsgIPCLink"
]
