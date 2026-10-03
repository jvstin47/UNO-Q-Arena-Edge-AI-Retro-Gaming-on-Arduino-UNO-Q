"""
Linux RPMsg Endpoint Link
Provides direct shared-memory inter-processor communication on embedded Linux.
"""

from typing import Optional, Tuple
import os
from uno_q_arena.ipc.protocol import BinaryProtocolCodec, Packet


class RPMsgIPCLink:
    """Manages /dev/rpmsgX character device communication on Qualcomm Linux."""

    def __init__(self, endpoint_path: str = "/dev/rpmsg0"):
        self.endpoint_path = endpoint_path
        self.fd: Optional[int] = None
        self._init_endpoint()

    def _init_endpoint(self) -> None:
        if os.path.exists(self.endpoint_path):
            try:
                self.fd = os.open(self.endpoint_path, os.O_RDWR | os.O_NONBLOCK)
                print(f"[IPC] RPMsg endpoint opened: {self.endpoint_path}")
            except Exception as e:
                print(f"[IPC] Could not open RPMsg endpoint: {e}")
                self.fd = None

    def connect(self) -> bool:
        if self.fd is None:
            self._init_endpoint()
        return self.is_connected

    @property
    def is_connected(self) -> bool:
        return self.fd is not None

    def read_packet(self) -> Optional[Packet]:
        if not self.is_connected:
            return None
        try:
            raw_bytes = os.read(self.fd, 8)
            if len(raw_bytes) >= 8:
                return BinaryProtocolCodec.decode(raw_bytes)
        except Exception:
            pass
        return None

    def send_packet(self, packet_bytes: bytes) -> bool:
        if not self.is_connected:
            return False
        try:
            os.write(self.fd, packet_bytes)
            return True
        except Exception:
            return False

    def read_inputs(self) -> Tuple[Optional[int], Optional[float]]:
        pkt = self.read_packet()
        if pkt:
            return pkt.controller.buttons, pkt.aggression_pct / 100.0
        return None, None

    def close(self) -> None:
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
