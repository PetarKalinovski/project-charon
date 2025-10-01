from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.elevenlabs_stt_processors import ElevenLabsSTTProcessor
from rich import print as rprint
import tracemalloc
import asyncio


tracemalloc.start()


async def main():
    stt_processor = ElevenLabsSTTProcessor()

    try:
        rprint("🎙️  [bold green]Starting voice input recording...[/bold green]")
        voice_input = await stt_processor.get_voice_input_elevenlabs_smart()

        if voice_input:
            rprint(f"🗣️  [bold green]Voice input received: {voice_input}[/bold green]")
        else:
            rprint("⚠️  [yellow]No voice input detected[/yellow]")

    except Exception as e:
        rprint(f"❌ [red]Error during voice input processing: {e}[/red]")


if __name__ == "__main__":
    asyncio.run(main())
