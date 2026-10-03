"""
Audio Output Manager
Streams 44.1 kHz 16-bit stereo PCM audio buffers to hardware speakers.
"""

from typing import Optional
import numpy as np
import pygame


class AudioManager:
    """Manages low-latency real-time PCM audio streaming via pygame.mixer."""

    def __init__(self, frequency: int = 44100, buffer_size: int = 512, enabled: bool = True):
        self.frequency = frequency
        self.buffer_size = buffer_size
        self.enabled = enabled
        self.muted = not enabled
        self.channel: Optional[pygame.mixer.Channel] = None
        if self.enabled:
            self._init_audio()

    def _init_audio(self) -> None:
        try:
            pygame.mixer.pre_init(
                frequency=self.frequency,
                size=-16,
                channels=2,
                buffer=self.buffer_size
            )
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.channel = pygame.mixer.Channel(0)
            print(f"[Audio] 44.1 kHz 16-bit Stereo PCM mixer initialized (buffer: {self.buffer_size}).")
        except Exception as e:
            print(f"[Audio] Mixer initialization warning: {e}")

    def start(self) -> None:
        if self.enabled and self.channel is None:
            self._init_audio()

    def stream_chunk(self, audio_samples: Optional[np.ndarray]) -> None:
        """Plays or queues an audio chunk."""
        if not self.enabled or self.muted or self.channel is None or audio_samples is None:
            return
        if len(audio_samples) == 0:
            return

        try:
            sound = pygame.sndarray.make_sound(audio_samples)
            if not self.channel.get_busy():
                self.channel.play(sound)
            elif self.channel.get_queue() is None:
                self.channel.queue(sound)
        except Exception:
            pass

    def queue_audio(self, audio_samples: Optional[np.ndarray]) -> None:
        self.stream_chunk(audio_samples)

    def toggle_mute(self) -> bool:
        """Toggles audio mute."""
        self.muted = not self.muted
        if self.muted and self.channel is not None:
            self.channel.stop()
        print(f"[Audio] Muted: {self.muted}")
        return self.muted

    def stop(self) -> None:
        self.close()

    def close(self) -> None:
        if pygame.mixer.get_init():
            pygame.mixer.quit()
