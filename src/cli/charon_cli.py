#!/usr/bin/env python3
"""
Charon CLI - Your Personal Assistant Ferryman
Guiding you through the complexities of daily life with intelligent task orchestration.
"""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich import box
from rich.align import Align
from rich.table import Table
import yaml


# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.agents.big_boss_orchestrator_agent import BigBossOrchestratorAgent
from src.utils.charon_ascii_art import CHARON_ART_ASCII, THE_FARRYMANS_ASSISTANT_ASCII
from src.utils.tts_callback_handler import initialize_tts, change_tts_voice
from src.schemas.config_schema import (
    Config,
    FilesAgentConfig,
    HomeAgentConfig,
    TaskAgentConfig,
    CalendarAgentConfig,
    GitHubAgentConfig,
    ModelConfig,
    BooksAgentConfig,
    MoviesAgentConfig,
    RecommenderAgentConfig,
    BigBossOrchestratorAgentConfig,
)
from src.utils.elevenlabs_stt_processors import ElevenLabsSTTProcessor

from strands.session.file_session_manager import FileSessionManager
import json
from dotenv import load_dotenv
import asyncio


load_dotenv()

# Initialize rich console and typer app
console = Console()
app = typer.Typer(
    name="charon",
    help="💀🛶  Charon - Your Personal Assistant Ferryman",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


class CharonCLI:
    def __init__(self):
        self.agent = None
        self.session_context = {}
        self.user_preferences = {}
        self.stt = False

    def display_banner(self):
        """Display the mythological Charon-themed banner"""
        banner = Text()
        banner.append(CHARON_ART_ASCII, style="bold magenta")
        banner.append(THE_FARRYMANS_ASSISTANT_ASCII, style="magenta")
        banner.append("")

        subtitle = Text(
            "Guiding you across the river of daily complexities\n"
            "Your intelligent orchestrator for work, leisure, and life management",
            style="italic dim white",
        )

        panel = Panel(
            Align.center(Text.assemble(banner, "\n\n", subtitle)),
            title="⚡ [bold yellow]Welcome Aboard[/bold yellow] ⚡",
            border_style="dark_magenta",
            box=box.DOUBLE,
            padding=(1, 2),
        )

        console.print()
        console.print(panel)
        console.print()

    def show_help_panel(self):
        """Show what users can do"""
        help_table = Table(show_header=False, box=box.MINIMAL)
        help_table.add_column("Category", style="bold cyan", width=15)
        help_table.add_column("Examples", style="white")

        help_table.add_row(
            "📋 Work Tasks", "Analyze my project • Schedule coding time • GitHub issues"
        )
        help_table.add_row(
            "🎭 Leisure", "What should I watch? • Recommend a book • YouTube videos"
        )
        help_table.add_row(
            "📅 Planning", "When am I free? • Block focus time • Schedule meeting"
        )
        help_table.add_row("⚙️ Control", "help • clear • exit • status •")
        help_table.add_row(
            "👥 Sessions", "sessions/show sessions • charon-switch-session <session_id>"
        )
        help_table.add_row(
            "⚒️ Config Wizard", "exit the process and run 'uv run charon.py setup'"
        )
        help_table.add_row(
            "🎧 Audio Settings",
            "audio on/off • charon-switch-voice <voice> [light|medium|heavy|none|heart]",
        )
        help_table.add_row(
            "🎙️ Voice Input",
            "charon-listen to toggle voice input mode on/off",
        )

        console.print("\n")
        console.print(help_table)
        console.print(
            "\n[dim]💡 Tip: Just describe what you need in natural language[/dim]"
        )

    def handle_command(self, user_input: str) -> bool:
        """Handle special commands, return True if handled"""
        if user_input.lower() in ["help", "?"]:
            self.show_help_panel()
            return True
        elif user_input.lower() in ["audio off", "mute"]:
            if self.user_preferences.get("audio", True):
                session_id = self.agent.get_session_id()
                session_manager = FileSessionManager(session_id=session_id)

                self.agent = BigBossOrchestratorAgent(
                    session_manager=session_manager, silent=True
                )

            self.user_preferences["audio"] = False
            console.print("🔇 Audio disabled")
            return True
        elif user_input.lower() in ["audio on", "unmute"]:
            if self.user_preferences.get("audio", False):
                session_id = self.agent.get_session_id()
                session_manager = FileSessionManager(session_id=session_id)
                self.agent = BigBossOrchestratorAgent(session_manager=session_manager)

            self.user_preferences["audio"] = True
            console.print("🔊 Audio enabled")
            initialize_tts()
            console.print("[dim]🔊 TTS system initialized[/dim]")
            return True
        elif user_input.lower() == "clear":
            console.clear()
            self.show_compact_banner()
            return True
        elif user_input.lower() == "status":
            self.show_status()
            return True

        elif user_input.lower() in ["sessions", "show sessions"]:
            self.show_sessions()
            return True

        elif user_input.lower().startswith("charon-switch-session "):
            session_id = user_input.split("charon-switch-session ")[-1].strip()
            self.change_session(session_id)
            return True

        elif user_input.lower().startswith("charon-switch-voice "):
            voice = user_input.split("charon-switch-voice ")[-1].strip()
            if voice not in ["light", "medium", "heavy", "none", "heart"]:
                console.print(
                    "[red]Invalid voice. Use: light, medium, heavy, none, or heart[/red]"
                )
                return True
            elif self.user_preferences.get("audio", True) is False:
                console.print(
                    "[yellow]Audio is disabled. Enable it with 'audio on'[/yellow]"
                )
                return True
            else:
                change_tts_voice(voice)
                console.print(f"[dim]👻 Voice changed to: {voice}[/dim]")
                return True

        elif user_input.lower().startswith("charon-listen"):
            if self.stt:
                self.stt = False
                console.print(
                    "[dim]🎙️  Voice input mode disabled. You can type your input now.[/dim]"
                )
                return True
            else:
                self.stt = True
                console.print(
                    "[dim]🎙️  Voice input mode enabled. Speak clearly to record your input.[/dim]"
                )
                return True

        return False

    def show_sessions(self):
        """Show all active sessions"""
        session_table = Table(title="All Sessions")
        session_table.add_column("Session ID", style="cyan")
        session_table.add_column("Description", style="green")

        # Load sessions from file
        path_to_sessions = (
            Path(__file__).parent.parent.parent
            / "data"
            / "sessions"
            / "session_ids.json"
        )
        try:
            with open(path_to_sessions) as f:
                sessions = json.load(f)
            for session in sessions:
                session_table.add_row(session["session_id"], session["description"])
        except FileNotFoundError:
            console.print("[red]No sessions found[/red]")
            return

        console.print("\n[bold] Here are all sessions:[/bold]")

        console.print(session_table)

        console.print("Active session:")
        if self.agent is None:
            console.print("[red]No active session[/red]")
            return
        console.print(f"[bold]Session ID:[/bold] {self.agent.get_session_id()}")

        console.print(
            "to change sessions use the command 'charon-switch-session <session_id>'"
        )

    def change_session(self, session_id: str):
        """Change to a different session"""
        path_to_sessions = (
            Path(__file__).parent.parent.parent
            / "data"
            / "sessions"
            / "session_ids.json"
        )
        try:
            with open(path_to_sessions) as f:
                sessions = json.load(f)

            for session in sessions:
                if session["session_id"] == session_id:
                    session_manager = FileSessionManager(session_id=session_id)
                    self.agent = BigBossOrchestratorAgent(
                        session_manager=session_manager
                    )
                    console.print(
                        f"[bold green]Switched to session:[/bold green] {session_id}"
                    )
                    return

            console.print(f"[red]Session ID {session_id} not found[/red]")
        except FileNotFoundError:
            console.print("[red]No sessions file found[/red]")

    def show_status(self):
        """Show system status"""
        status_table = Table(title="System Status")
        status_table.add_column("Component", style="cyan")
        status_table.add_column("Status", style="green")

        # Check each agent's availability
        if self.agent:
            status_table.add_row("Big Boss Orchestrator Agent", "✅ Active")
            status_table.add_row("Model", f"[bold]{self.agent.model_id}[/bold]")
            status_table.add_row(
                "Session Id",
                f"[bold]{self.agent.get_session_id()}[/bold]",
            )
        else:
            status_table.add_row("Big Boss Orchestrator Agent", "❌ Inactive")

        status_table.add_row(
            "Audio", "🔊 On" if self.user_preferences.get("audio", True) else "🔇 Off"
        )

        console.print(status_table)

    def run_stt_chat(self) -> Optional[str]:
        stt = ElevenLabsSTTProcessor()
        try:
            console.print(
                "🎙️  [bold green]Starting voice input recording...[/bold green]"
            )
            voice_input = asyncio.run(stt.get_voice_input_elevenlabs_smart())

            if voice_input:
                console.print(f"[bold white]💬 You: {voice_input}[/bold white]")
                return voice_input

            else:
                console.print("⚠️  [yellow]No voice input detected[/yellow]")
                return None

        except KeyboardInterrupt:
            console.print("\n[yellow]Voice input recording stopped[/yellow]")
            self.stt = False
            return "No input recorded1111"

        except Exception as e:
            console.print(f"❌ [red]Error: {e}[/red]")

    def run_chat(self):
        """Run the interactive chat loop"""
        while True:
            try:
                if not self.stt:
                    user_input = Prompt.ask("[bold white]💬 You", console=console)

                    if user_input.lower() in ["exit", "quit", "bye"]:
                        if Confirm.ask("Ready to disembark?"):
                            console.print(
                                "[bold magenta] 🛶 Farewell, traveler![/bold magenta]"
                            )
                            break
                        continue

                    if self.handle_command(user_input):
                        continue

                if self.stt:
                    user_input = self.run_stt_chat()

                if user_input == "No input recorded1111":
                    continue

                if not self.agent:
                    with console.status(
                        "[bold magenta]Initializing Charon...", spinner="dots"
                    ):
                        if self.user_preferences.get("audio", True):
                            self.agent = BigBossOrchestratorAgent()
                        else:
                            self.agent = BigBossOrchestratorAgent(silent=True)

                self.agent.query(user_input)

            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit gracefully[/yellow]")
                continue
            except Exception as e:
                console.print(f"[red]❌ Something went wrong: {str(e)}[/red]")
                console.print("[dim]Try rephrasing your request or type 'help'[/dim]")


@app.command()
def chat(
    minimal: bool = typer.Option(
        False, "--minimal", "-m", help="Start with minimal UI"
    ),
    audio: bool = typer.Option(True, "--audio/--no-audio", help="Enable/disable audio"),
):
    """Start interactive chat with Charon"""

    cli = CharonCLI()
    cli.user_preferences["audio"] = audio

    try:
        # Minimal startup
        if not minimal:
            cli.display_banner()
            # cli.show_help_panel()

        console.print(
            "🛶 [bold magenta]Ready![/bold magenta] What would you like to do?\n"
        )
        if cli.user_preferences.get("audio", True):
            initialize_tts()

        cli.run_chat()

    except Exception as e:
        console.print(f"[red]Failed to start Charon: {str(e)}[/red]")
        raise typer.Exit(1)

    # Graceful exit


@app.command()
def setup():
    """Interactive setup wizard"""
    console.print("🛶 [bold magenta]Charon Setup Wizard 🧙[/bold magenta]\n")

    # Check for required files/configs
    console.print("Checking configuration...")

    # Guide user through setup
    if not Path("config/project-config.yaml").exists():
        console.print("[yellow]⚠️  Configuration file not found[/yellow]")
        console.print("I'll help you create one...")
        console.print("Please follow the prompts to set up your project configuration.")

    console.print("Write your root directory for the files agent:")
    root_directory = Prompt.ask(
        "[bold white]Root Directory[/bold white]",
        default="home/petar/Documents",
    )

    console.print(f"Root directory set to: {root_directory}")

    console.print("Do you want to use the same model for all agents? (y/n)")
    use_default_model = Confirm.ask(
        "[bold white]Use same model for all agents?[/bold white]",
        default=True,
    )

    if use_default_model:
        console.print("What model do you want to use for all agents?")
        console.print(
            "Examples: \n"
            "- us.anthropic.claude-sonnet-4-20250514-v1:0 \n"
            "- openrouter/mistralai/devstral-small"
        )

        console.print(
            " If not using Anthropic, it is recommended to not use the same model for all agents. For eg use devstral-medium for the orchestrators."
        )
        model_id = Prompt.ask(
            "[bold white]Model ID[/bold white]",
            default="us.anthropic.claude-sonnet-4-20250514-v1:0",
        )
        console.print(f"Model ID set to: {model_id}")

    elif not use_default_model:
        console.print(
            "You can set different models for each agent later in the config file."
        )
        model_id = None

    console.print("Write github username for the GitHub agent:")
    github_username = Prompt.ask(
        "[bold white]GitHub Username[/bold white]",
        default="PetarKalinovski",
    )
    console.print(f"GitHub username set to: {github_username}")

    config = Config(
        files_agent=FilesAgentConfig(
            root_directory=root_directory,
            model=ModelConfig(
                model_id=model_id
                if (use_default_model and model_id is not None)
                else "us.anthropic.claude-sonnet-4-20250514-v1:0"
            ),
        ),
        calendar_agent=CalendarAgentConfig(
            model=ModelConfig(
                model_id=model_id
                if (use_default_model and model_id is not None)
                else "us.anthropic.claude-sonnet-4-20250514-v1:0"
            )
        ),
        task_agent=TaskAgentConfig(
            model=ModelConfig(
                model_id=model_id
                if (use_default_model and model_id is not None)
                else "us.anthropic.claude-sonnet-4-20250514-v1:0"
            )
        ),
        github_agent=GitHubAgentConfig(
            model=ModelConfig(
                model_id=model_id
                if (use_default_model and model_id is not None)
                else "us.anthropic.claude-sonnet-4-20250514-v1:0"
            ),
            github_username=github_username,
        ),
        books_agent=BooksAgentConfig(
            model=ModelConfig(
                model_id=model_id
                if (use_default_model and model_id is not None)
                else "us.anthropic.claude-sonnet-4-20250514-v1:0"
            ),
            book_list_file="data/book_list.json",
        ),
        movies_agent=MoviesAgentConfig(
            model=ModelConfig(
                model_id=model_id
                if (use_default_model and model_id is not None)
                else "us.anthropic.claude-sonnet-4-20250514-v1:0"
            ),
            movie_list_file="data/movie_and_show.json",
        ),
        recommender_agent=RecommenderAgentConfig(
            model=ModelConfig(
                model_id=model_id
                if (use_default_model and model_id is not None)
                else "us.anthropic.claude-sonnet-4-20250514-v1:0"
            ),
            substack_newsletters_file="data/substack_newsletters.json",
            youtube_channels_file="data/youtube_channels.json",
        ),
        home_agent=HomeAgentConfig(
            model=ModelConfig(
                model_id=model_id
                if (use_default_model and model_id is not None)
                else "us.anthropic.claude-sonnet-4-20250514-v1:0"
            )
        ),
        big_boss_orchestrator_agent=BigBossOrchestratorAgentConfig(
            model=ModelConfig(
                model_id=model_id
                if (use_default_model and model_id is not None)
                else "us.anthropic.claude-sonnet-4-20250514-v1:0"
            ),
            sleep_tracking_file="data/sleep_tracking.json",
        ),
    )

    # Save the config to a YAML file
    config_path = Path("config/project-config-generated.yaml")

    yaml_config = yaml.dump(config.model_dump(), sort_keys=False)

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        f.write(yaml_config)

    console.print(
        "✅ Setup complete! Run 'uv run charon.py chat' to get started. If you want to change the config manually, edit the file at:",
        style="bold green",
    )
    console.print(config_path, style="bold green")


if __name__ == "__main__":
    app()
