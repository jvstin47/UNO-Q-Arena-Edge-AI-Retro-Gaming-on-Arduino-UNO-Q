"""
Serial UART IPC Link
Provides serial port communication with the Arduino UNO Q / STM32 coprocessor.
"""

from typing import Optional, Tuple
import serial
from uno_q_arena.ipc.protocol import (
    BinaryProtocolCodec,
    Packet,
    deserialize_input_packet,
    serialize_telemetry_packet,
    serialize_haptic_packet
)


class SerialIPCLink:
    """Manages high-speed UART connection to STM32."""

    def __init__(self, port: str = "/dev/ttyACM0", baudrate: int = 115200, timeout: float = 0.002):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser: Optional[serial.Serial] = None
        self._connect()

    def _connect(self) -> None:
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"[IPC] Connected to STM32 hardware at {self.port} @ {self.baudrate} baud.")
        except Exception:
            # Silent fallback when running on host without physical board connected
            self.ser = None

    def connect(self) -> bool:
        if self.ser is None or not self.ser.is_open:
            self._connect()
        return self.is_connected

    @property
    def is_connected(self) -> bool:
        return self.ser is not None and self.ser.is_open

    def read_packet(self) -> Optional[Packet]:
        """Reads and decodes latest packet from STM32."""
        if not self.is_connected:
            return None
        try:
            if self.ser.in_waiting >= 8:
                raw_bytes = self.ser.read(8)
                return BinaryProtocolCodec.decode(raw_bytes)
        except Exception:
            pass
        return None

    def send_packet(self, packet_bytes: bytes) -> bool:
        """Sends raw encoded packet to STM32."""
        if not self.is_connected:
            return False
        try:
            self.ser.write(packet_bytes)
            return True
        except Exception:
            return False

    def read_inputs(self) -> Tuple[Optional[int], Optional[float]]:
        """Reads latest controller state and aggression knob from STM32."""
        if not self.is_connected:
            return None, None
        try:
            if self.ser.in_waiting >= 8:
                raw_bytes = self.ser.read(8)
                res = deserialize_input_packet(raw_bytes)
                if res is not None:
                    return res
        except Exception:
            pass
        return None, None

    def send_telemetry(self, p1_hp: int, p2_hp: int, latency_us: int, action_id: int) -> None:
        """Sends match state to STM32 to drive OLED and NeoPixel LEDs."""
        if not self.is_connected:
            return
        try:
            packet = serialize_telemetry_packet(p1_hp, p2_hp, latency_us, action_id)
            self.ser.write(packet)
        except Exception:
            pass

    def send_haptic_trigger(self, severity: int, duration_ms: int) -> None:
        """Sends haptic hit vibration command to STM32."""
        if not self.is_connected:
            return
        try:
            packet = serialize_haptic_packet(severity, duration_ms)
            self.ser.write(packet)
        except Exception:
            pass

    def close(self) -> None:
        if self.ser is not None and self.ser.is_open:
            self.ser.close()
            self.ser = None
