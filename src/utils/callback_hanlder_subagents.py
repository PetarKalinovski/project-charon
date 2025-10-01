from rich.panel import Panel
from rich import print as rprint
from rich.padding import Padding
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.agent_session_tracker import AgentSessionTracker

# Global session tracker
session_tracker = AgentSessionTracker()

AGENT_STYLES = {
    "book_agent": {
        "emoji": "📚",
        "name": "Book Agent",
        "color": "green",
        "padding": (0, 0, 0, 16),
    },
    "movie_agent": {
        "emoji": "🎬",
        "name": "Movie Agent",
        "color": "red",
        "padding": (0, 0, 0, 16),
    },
    "recommender_agent": {
        "emoji": "⏯️",
        "name": "Recommender Agent",
        "color": "dark_blue",
        "padding": (0, 0, 0, 16),
    },
    "file_agent": {
        "emoji": "📂",
        "name": "File Agent",
        "color": "blue",
        "padding": (0, 0, 0, 24),
    },
    "calendar_agent": {
        "emoji": "📅",
        "name": "Calendar Agent",
        "color": "red",
        "padding": (0, 0, 0, 24),
    },
    "github_agent": {
        "emoji": "🐙",
        "name": "GitHub Agent",
        "color": "blue",
        "padding": (0, 0, 0, 24),
    },
}


def log_to_session(message: str):
    """Log a message to the current session"""
    if session_tracker.active_session:
        session_tracker.session_print(message)
    else:
        rprint(f"[dim]{message}[/dim]")


def home_agent_callback(**kwargs):
    """Home Agent callback with session grouping"""

    if "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
        tool_use = kwargs["current_tool_use"]
        tool_name = tool_use.get("name")
        tool_input = tool_use.get("input", "")

        if tool_name in [
            "book_agent_query",
            "movies_agent_query",
            "recommender_agent_query",
        ]:
            try:
                if tool_input and tool_input.endswith('"}'):
                    parsed_input = json.loads(tool_input)
                    query = parsed_input.get("query", "")

                    # Map tool name to agent style
                    agent_mapping = {
                        "book_agent_query": "book_agent",
                        "movies_agent_query": "movie_agent",
                        "recommender_agent_query": "recommender_agent",
                    }

                    agent_key = agent_mapping.get(tool_name)
                    if agent_key and agent_key in AGENT_STYLES:
                        session_tracker.start_session(
                            agent_key, query, AGENT_STYLES[agent_key]
                        )

            except json.JSONDecodeError:
                pass

    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                # If we're in a session, use session styling, otherwise use default
                if session_tracker.active_session:
                    session_tracker.session_print(text, is_main_response=True)
                    session_tracker.end_session()
                else:
                    # Default home agent styling
                    rprint(
                        Padding(
                            Panel(
                                f" [cyan] 🎭 Home Agent: [/cyan] {text}",
                                title="🎭 Home Agent",
                                subtitle="Ready for leisure & entertainment",
                                border_style="cyan",
                            ),
                            pad=(0, 0, 0, 8),
                        )
                    )


def task_agent_callback(**kwargs):
    """Task Agent callback with session grouping"""

    if "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
        tool_use = kwargs["current_tool_use"]
        tool_name = tool_use.get("name")
        tool_input = tool_use.get("input", "")

        if tool_name in [
            "file_search_agent_query",
            "google_calendar_agent_query",
            "github_agent_query",
        ]:
            try:
                if tool_input and tool_input.endswith('"}'):
                    parsed_input = json.loads(tool_input)
                    query = parsed_input.get("query", "")

                    agent_mapping = {
                        "file_search_agent_query": "file_agent",
                        "google_calendar_agent_query": "calendar_agent",
                        "github_agent_query": "github_agent",
                    }

                    agent_key = agent_mapping.get(tool_name)
                    if agent_key and agent_key in AGENT_STYLES:
                        session_tracker.start_session(
                            agent_key, query, AGENT_STYLES[agent_key]
                        )

            except json.JSONDecodeError:
                pass

    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                if session_tracker.active_session:
                    session_tracker.session_print(text, is_main_response=True)
                    session_tracker.end_session()
                else:
                    rprint(
                        Padding(
                            Panel(
                                f" [green] 📝 Task Agent: [/green] {text}",
                                title="📝 Task Agent",
                                subtitle="Ready to manage your tasks",
                                border_style="green",
                            ),
                            pad=(0, 0, 0, 8),
                        )
                    )


def book_agent_callback(**kwargs):
    """Book Agent callback that respects sessions"""
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                if session_tracker.active_session == "book_agent":
                    session_tracker.session_print(text)
                else:
                    rprint(
                        Padding(
                            Panel(
                                f" [green] 📚 Book Agent: [/green] {text}",
                                title="📚 Book Agent",
                                subtitle="Ready to manage your book collection",
                                border_style="green",
                            ),
                            pad=(0, 0, 0, 16),
                        )
                    )


def movie_agent_callback(**kwargs):
    """Movie Agent callback that respects sessions"""
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                if session_tracker.active_session == "movie_agent":
                    session_tracker.session_print(text)
                else:
                    rprint(
                        Padding(
                            Panel(
                                f" [red] 🎬 Movie Agent: [/red] {text}",
                                title="🎬 Movie Agent",
                                subtitle="Ready to manage your movie collection",
                                border_style="red",
                            ),
                            pad=(0, 0, 0, 16),
                        )
                    )


def recommender_agent_callback(**kwargs):
    """Recommender Agent callback that respects sessions"""
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                if session_tracker.active_session == "recommender_agent":
                    session_tracker.session_print(text)
                else:
                    rprint(
                        Padding(
                            Panel(
                                f" [dark_blue] ⏯️ Recommender Agent: [/dark_blue] {text}",
                                title="⏯️ Recommender Agent",
                                subtitle="Ready for youtube or substack recommendations",
                                border_style="dark_blue",
                            ),
                            pad=(0, 0, 0, 16),
                        )
                    )


def file_agent_callback(**kwargs):
    """File Agent callback that respects sessions"""
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                if session_tracker.active_session == "file_agent":
                    session_tracker.session_print(text)
                else:
                    rprint(
                        Padding(
                            Panel(
                                f" [blue] 📂 File Agent: [/blue] {text}",
                                title="📂 File Agent",
                                subtitle="Ready to manage your files",
                                border_style="blue",
                            ),
                            pad=(0, 0, 0, 24),
                        )
                    )


def calendar_agent_callback(**kwargs):
    """Calendar Agent callback that respects sessions"""
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                if session_tracker.active_session == "calendar_agent":
                    session_tracker.session_print(text)
                else:
                    rprint(
                        Padding(
                            Panel(
                                f" [red] 📅 Calendar Agent: [/red] {text}",
                                title="📅 Calendar Agent",
                                subtitle="Ready to manage your calendar",
                                border_style="red",
                            ),
                            pad=(0, 0, 0, 24),
                        )
                    )


def github_agent_callback(**kwargs):
    """GitHub Agent callback that respects sessions"""
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        for content in kwargs["message"]["content"]:
            if isinstance(content, dict) and "text" in content:
                text = content["text"]

                if session_tracker.active_session == "github_agent":
                    session_tracker.session_print(text)
                else:
                    rprint(
                        Padding(
                            Panel(
                                f" [blue] 🐙 GitHub Agent: [/blue] {text}",
                                title="🐙 GitHub Agent",
                                subtitle="Ready to manage your GitHub repositories",
                                border_style="blue",
                            ),
                            pad=(0, 0, 0, 24),
                        )
                    )
