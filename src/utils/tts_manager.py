from kokoro import KPipeline
import sounddevice as sd
import numpy as np
from rich import print as rprint
from typing import Optional
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.demonic_voice_processor import DemonicVoiceProcessor
import queue
import threading


class TTSManager:
    """Singleton TTS manager that initializes Kokoro only once"""

    _instance: Optional["TTSManager"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.pipeline = None
            self.voice_blend = None
            self.voice_processor = DemonicVoiceProcessor()
            self.demonic_intensity = "medium"
            self._load_tts()
            TTSManager._initialized = True

    def _load_tts(self):
        """Initialize the TTS pipeline and voices once"""
        try:
            rprint("[dim]🔊 Initializing TTS system...[/dim]")

            self.pipeline = KPipeline(lang_code="a")

            bm_lewis = self.pipeline.load_voice("bm_lewis")
            am_michael = self.pipeline.load_voice("am_michael")

            self.voice_blend = np.add(bm_lewis * 0.8, am_michael * 0.2)

            rprint("[dim]💀 Charon's voice is ready to ferry your words...[/dim]")

        except Exception as e:
            rprint(f"[red]❌ Failed to initialize TTS: {e}[/red]")
            self.pipeline = None
            self.voice_blend = None

    def set_demonic_intensity(self, intensity: str):
        """Set the demonic intensity for voice effects"""
        if intensity in ["light", "medium", "heavy", "none", "heart"]:
            self.demonic_intensity = intensity
            rprint(f"[dim]👹 Demonic intensity set to: {intensity}[/dim]")
        else:
            rprint(
                "[yellow]⚠️ Invalid intensity. Use: light, medium, heavy, none, or heart[/yellow]"
            )

    def is_available(self) -> bool:
        """Check if TTS is available"""
        return self.pipeline is not None and self.voice_blend is not None

    def speak(self, text: str, speed: float = 1.1) -> bool:
        """Stream TTS with parallel generation and playback"""
        if not self.is_available():
            return False

        try:
            # Clean up text for TTS
            formatted_parts = [
                part.strip() for part in text.split("\n") if part.strip()
            ]

            clean_parts = []
            for part in formatted_parts:
                clean_part = (
                    part.replace("**", "")
                    .replace("[", "")
                    .replace("]", "")
                    .replace("#", "")
                )
                clean_parts.append(clean_part)

            text_readable = "\n".join(clean_parts)

            # Create queue for audio chunks
            audio_queue = queue.Queue()
            generation_complete = threading.Event()

            def audio_generator():
                """Generate audio chunks in background thread"""
                try:
                    if self.demonic_intensity == "heart":
                        generator = self.pipeline(
                            text_readable,
                            voice="af_heart",
                            speed=speed,
                            split_pattern=r"\n+",
                        )
                    else:
                        generator = self.pipeline(
                            text_readable,
                            voice=self.voice_blend,
                            speed=speed,
                            split_pattern=r"\n+",
                        )

                        # Process each chunk as it comes from the generator
                    for i, (gs, ps, audio) in enumerate(generator):
                        try:
                            # Apply demonic effects to this chunk
                            demonic_audio = self.voice_processor.apply_demonic_effects(
                                audio, self.demonic_intensity
                            )

                            # Put in queue with text part
                            formatted_part = (
                                formatted_parts[i] if i < len(formatted_parts) else ""
                            )
                            audio_queue.put(
                                (formatted_part, demonic_audio, False)
                            )  # False = not the last chunk

                        except Exception as e:
                            rprint(
                                f"[yellow]⚠️ Effect failed for chunk {i}: {e}[/yellow]"
                            )
                            # Fallback to normal audio
                            audio_np = (
                                audio.detach().cpu().numpy()
                                if hasattr(audio, "detach")
                                else np.array(audio)
                            )
                            formatted_part = (
                                formatted_parts[i] if i < len(formatted_parts) else ""
                            )
                            audio_queue.put((formatted_part, audio_np, False))

                    # Signal completion
                    audio_queue.put((None, None, True))  # True = last chunk marker
                    generation_complete.set()

                except Exception as e:
                    rprint(f"[red]Generation error: {e}[/red]")
                    audio_queue.put((None, None, True))
                    generation_complete.set()

            # Start generation in background
            generation_thread = threading.Thread(target=audio_generator, daemon=True)
            generation_thread.start()

            # Play audio chunks as they become available
            while True:
                try:
                    # Wait for next chunk (with timeout to avoid hanging)
                    formatted_part, demonic_audio, is_last = audio_queue.get(
                        timeout=10.0
                    )

                    if is_last:  # End marker
                        break

                    if formatted_part and demonic_audio is not None:
                        # Display text immediately
                        rprint(f"{formatted_part}")

                        sd.play(demonic_audio, 24000)
                        sd.wait()

                except queue.Empty:
                    rprint("[yellow]⚠️ Timeout waiting for audio chunk[/yellow]")
                    break
                except Exception as e:
                    rprint(f"[red]Playback error: {e}[/red]")
                    break

            return True

        except Exception as e:
            rprint(f"[red]Streaming TTS Error: {e}[/red]")
            return False

        except Exception as e:
            rprint(f"[red]TTS Error: {e}[/red]")
            return False
