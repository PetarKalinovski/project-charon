import numpy as np
import scipy.signal


class DemonicVoiceProcessor:
    """Audio effects processor to make Charon sound demonic/otherworldly"""

    def __init__(self, sample_rate: int = 24000):
        self.sample_rate = sample_rate
        self.reverb_delay = int(0.1 * sample_rate)  # 100ms delay for reverb
        self.reverb_buffer = np.zeros(self.reverb_delay)

    def _tensor_to_numpy(self, audio) -> np.ndarray:
        """Safely convert tensor/array to numpy array"""
        if hasattr(audio, "detach"):  # PyTorch tensor
            audio = audio.detach().cpu().numpy()
        elif hasattr(audio, "numpy"):  # Other tensor types
            audio = audio.numpy()

        return np.array(audio, dtype=np.float32)

    def pitch_shift(self, audio, shift_factor: float = 0.75) -> np.ndarray:
        """
        Lower the pitch to make voice deeper and more ominous.
        shift_factor < 1.0 = lower pitch (more demonic)
        shift_factor > 1.0 = higher pitch
        """
        audio = self._tensor_to_numpy(audio)

        # Simple pitch shifting using resampling
        shifted_length = int(len(audio) / shift_factor)

        # Resample to change pitch
        shifted = scipy.signal.resample(audio, shifted_length)

        return shifted.astype(np.float32)

    def add_reverb(self, audio, decay: float = 0.3, mix: float = 0.4) -> np.ndarray:
        """
        Add cavernous reverb effect for otherworldly atmosphere.
        decay: how much the echo fades (0.0-1.0)
        mix: how much reverb to blend in (0.0-1.0)
        """
        audio = self._tensor_to_numpy(audio)
        reverb = np.zeros_like(audio)

        for i in range(len(audio)):
            # Add current sample to reverb buffer
            self.reverb_buffer[i % self.reverb_delay] = audio[i] + (
                decay * self.reverb_buffer[i % self.reverb_delay]
            )

            # Get delayed sample for reverb
            reverb[i] = self.reverb_buffer[
                (i - self.reverb_delay + 1) % self.reverb_delay
            ]

        # Mix original with reverb
        return audio * (1 - mix) + reverb * mix

    def add_distortion(self, audio, drive: float = 2.0, mix: float = 0.2) -> np.ndarray:
        """
        Add subtle distortion for a more menacing quality.
        drive: amount of distortion (1.0+ = more distortion)
        mix: how much distorted signal to blend in
        """
        audio = self._tensor_to_numpy(audio)

        # Soft clipping distortion
        distorted = np.tanh(audio * drive) / drive

        # Mix with original
        return audio * (1 - mix) + distorted * mix

    def add_chorus(
        self, audio, rate: float = 2.0, depth: float = 0.002, mix: float = 0.3
    ) -> np.ndarray:
        """
        Add chorus effect for ethereal, otherworldly quality.
        rate: LFO frequency in Hz
        depth: modulation depth in seconds
        mix: wet/dry mix
        """
        audio = self._tensor_to_numpy(audio)

        # Create LFO (Low Frequency Oscillator)
        t = np.arange(len(audio)) / self.sample_rate
        lfo = np.sin(2 * np.pi * rate * t)

        # Modulated delay in samples
        delay_samples = depth * self.sample_rate * (1 + lfo)

        chorus = np.zeros_like(audio)

        for i, delay in enumerate(delay_samples):
            delay_int = int(delay)
            if i >= delay_int:
                chorus[i] = audio[i - delay_int]

        return audio * (1 - mix) + chorus * mix

    def low_pass_filter(self, audio, cutoff: float = 8000) -> np.ndarray:
        """
        Apply low-pass filter to make voice sound more distant/muffled.
        cutoff: frequency in Hz where higher frequencies start getting cut
        """
        audio = self._tensor_to_numpy(audio)
        nyquist = self.sample_rate / 2
        normalized_cutoff = cutoff / nyquist

        # Design low-pass filter
        b, a = scipy.signal.butter(4, normalized_cutoff, btype="low")

        # Apply filter
        return scipy.signal.filtfilt(b, a, audio)

    def apply_demonic_effects(self, audio, intensity: str = "medium") -> np.ndarray:
        """
        Apply the full demonic voice transformation.
        intensity: "light", "medium", "heavy" - how demonic to make it
        """
        # Convert tensor to numpy array if needed
        audio = self._tensor_to_numpy(audio)

        if intensity == "light":
            # Subtle otherworldly effects
            audio = self.pitch_shift(audio, 0.85)  # Slightly lower pitch
            audio = self.add_reverb(audio, decay=0.2, mix=0.2)
            audio = self.add_chorus(audio, mix=0.1)
            audio = self.add_distortion(audio, drive=1.5, mix=0.1)
            audio = self.low_pass_filter(audio, 7000)

        elif intensity == "medium":
            # Noticeable demonic quality
            audio = self.pitch_shift(audio, 0.85)
            audio = self.add_reverb(audio, decay=0.3, mix=0.4)
            audio = self.add_distortion(audio, drive=1.5, mix=0.1)
            audio = self.add_chorus(audio, mix=0.2)
            audio = self.low_pass_filter(audio, 7000)

        elif intensity == "heavy":
            # Very demonic/otherworldly
            audio = self.pitch_shift(audio, 0.65)  # Much lower pitch
            audio = self.add_reverb(audio, decay=0.4, mix=0.5)
            audio = self.add_distortion(audio, drive=2.0, mix=0.2)
            audio = self.add_chorus(audio, mix=0.3)
            audio = self.low_pass_filter(audio, 6000)

        # Normalize output to prevent clipping
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val * 0.8  # Leave some headroom
        return audio
