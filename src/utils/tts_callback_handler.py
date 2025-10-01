from rich import print as rprint
from rich.status import Status
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.tts_manager import TTSManager

tts_manager = TTSManager()


def tts_callback_handler(**kwargs):
    """
    Optimized callback handler that reuses TTS initialization.
    """
    with Status(
        "[bold dark_magenta]Navigating your request...",
        spinner="bouncingBar",
    ):
        if "message" in kwargs and kwargs["message"].get("role") == "assistant":
            for content in kwargs["message"]["content"]:
                if isinstance(content, dict) and "text" in content:
                    text = content["text"]

                    rprint("\n [bold dark_magenta]💀🛶 Charon:[/bold dark_magenta]")

                    if tts_manager.is_available():
                        tts_manager.speak(text)
                    else:
                        rprint(text)

        if "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
            tool_use = kwargs["current_tool_use"]
            tool_name = tool_use.get("name")
            tool_input = tool_use.get("input", "")
            if tool_name in ["home_agent_query", "task_agent_query"]:
                try:
                    if tool_input and tool_input.endswith('"}'):
                        parsed_input = json.loads(tool_input)
                        query = parsed_input.get("query", "")

                        agent_name = (
                            tool_name.replace("_query", "").replace("_", " ").title()
                        )

                        rprint(f"\n🔄 [bold cyan]Consulting {agent_name}[/bold cyan]")
                        rprint(f"   [dim]Query: {query}[/dim]")

                except json.JSONDecodeError:
                    pass
                except Exception as e:
                    rprint(f"[dim red]Debug: Error parsing tool input: {e}[/dim red]")


def silent_callback_handler(**kwargs):
    """
    Silent callback handler (no TTS, just text).
    """
    with Status(
        "[bold dark_magenta]Navigating your request...",
        spinner="bouncingBar",
    ):
        if "message" in kwargs and kwargs["message"].get("role") == "assistant":
            for content in kwargs["message"]["content"]:
                if isinstance(content, dict) and "text" in content:
                    text = content["text"]

                    rprint("\n [bold dark_magenta]💀🛶 Charon: [/bold dark_magenta]")
                    rprint(text)

        if "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
            tool_use = kwargs["current_tool_use"]
            tool_name = tool_use.get("name")
            tool_input = tool_use.get("input", "")
            if tool_name in ["home_agent_query", "task_agent_query"]:
                try:
                    if tool_input and tool_input.endswith('"}'):
                        parsed_input = json.loads(tool_input)
                        query = parsed_input.get("query", "")

                        agent_name = (
                            tool_name.replace("_query", "").replace("_", " ").title()
                        )

                        rprint(f"\n🔄 [bold cyan]Consulting {agent_name}[/bold cyan]")
                        rprint(f"   [dim]Query: {query}[/dim]")

                except json.JSONDecodeError:
                    pass
                except Exception as e:
                    rprint(f"[dim red]Debug: Error parsing tool input: {e}[/dim red]")


def initialize_tts():
    global tts_manager


def change_tts_voice(voice: str):
    global tts_manager
    tts_manager.set_demonic_intensity(voice)
