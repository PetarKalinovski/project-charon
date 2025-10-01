import sounddevice as sd
import numpy as np
import asyncio
from typing import Optional
from rich import print as rprint
import tempfile
import wave
from elevenlabs.client import ElevenLabs
import os
from dotenv import load_dotenv

load_dotenv()


class ElevenLabsSTTProcessor:
    def __init__(self):
        self.elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.sample_rate = 16000
        self.chunk_duration = 0.1  # 100ms chunks
        self.chunk_size = int(self.sample_rate * self.chunk_duration)
        self.silence_threshold = 0.01  # Adjust based on your microphone
        self.silence_chunks_needed = 20  # 2 seconds of silence to stop

    async def get_voice_input_elevenlabs_smart(self) -> Optional[str]:
        """
        Record with voice activity detection - automatically stops when speech ends
        """
        # Voice activity detection parameters
        # Silence detection
        audio_buffer = []
        silence_counter = 0
        recording = True

        rprint(
            "🎙️  [bold green]Listening... (speak clearly, will auto-stop)[/bold green]"
        )

        def audio_callback(indata, frames, time, status):
            nonlocal audio_buffer, silence_counter, recording

            if recording:
                # Calculate RMS (volume level)
                rms = np.sqrt(np.mean(indata**2))

                # Add chunk to buffer
                audio_buffer.append(indata.copy())

                # Check for silence
                if rms < self.silence_threshold:
                    silence_counter += 1
                    if silence_counter >= self.silence_chunks_needed:
                        recording = False
                else:
                    silence_counter = 0

        # Start recording stream
        with sd.InputStream(
            callback=audio_callback,
            channels=1,
            samplerate=self.sample_rate,
            blocksize=self.chunk_size,
            dtype=np.float32,
        ):
            # Wait for recording to complete
            max_wait = 30  # Maximum 30 seconds
            wait_time = 0

            while recording and wait_time < max_wait:
                await asyncio.sleep(0.1)
                wait_time += 0.1

        if not audio_buffer:
            rprint("⚠️  [yellow]No audio recorded[/yellow]")
            return None

        try:
            full_audio = np.concatenate(audio_buffer, axis=0)

            # Step 2: Convert from float32 to int16 (WAV format requirement)
            # Normalize and convert to 16-bit PCM
            full_audio = np.clip(full_audio, -1.0, 1.0)  # Ensure values are in [-1, 1]
            audio_int16 = (full_audio * 32767).astype(np.int16)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name

            with wave.open(temp_file.name, "w") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_int16.tobytes())

            with open(temp_filename, "rb") as audio_file:
                transcript_response = self.elevenlabs.speech_to_text.convert(
                    file=audio_file,
                    model_id="scribe_v1",  # Model to use, for now only "scribe_v1" is supported
                    tag_audio_events=True,  # Tag audio events like laughter, applause, etc.
                    language_code="eng",  # Language of the audio file. If set to None, the model will detect the language automatically.
                    diarize=True,  # Whether to annotate who is speaking
                )

            os.unlink(temp_filename)

            transcript = transcript_response.text

            if transcript and transcript.strip():
                return transcript.strip()
            else:
                rprint("⚠️  [yellow]No speech detected in audio[/yellow]")
                return None

        except Exception as e:
            rprint(f"❌ [red]Error processing audio: {e}[/red]")
            return None
