from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.agents.agent import AgentAbstract
from src.tools.big_boss_orchestrator_tools import (
    home_agent_query,
    task_agent_query,
)
from src.tools.sleep_tracking_tools import (
    add_sleep_data,
    get_sleep_data,
    update_weekly_summary,
)
from src.utils.prompts import BIG_BOSS_ORCHESTRATOR_AGENT_PROMPT
from src.utils.tts_callback_handler import tts_callback_handler, silent_callback_handler
from strands_tools import journal
from strands.session.file_session_manager import FileSessionManager
from datetime import datetime
import json
from loguru import logger


class BigBossOrchestratorAgent(AgentAbstract):
    """
    The Big Boss Orchestrator Agent that coordinates between different agents.
    It can query the Task Agent and Home Agent.
    """

    def __init__(self, session_manager=None, silent=False):
        """
        Initialize the Big Boss Orchestrator Agent.

        Args:
            silent (bool): If True, the agent will operate in silent mode.
        """
        self.silent = silent

        self.session_id = self.generate_session_id()
        self.session_manager = session_manager

        super().__init__()

    def get_agent_config(self):
        """Return the specific configuration section for this agent."""
        return self.config.big_boss_orchestrator_agent

    def get_prompt(self):
        """Return the system prompt for this agent."""
        return BIG_BOSS_ORCHESTRATOR_AGENT_PROMPT

    def get_tools(self):
        """Return the list of tools available for this agent."""
        return [
            task_agent_query,
            home_agent_query,
            add_sleep_data,
            get_sleep_data,
            update_weekly_summary,
            journal,
        ]

    def pass_callback_handler(self):
        """
        Pass a callback handler to the agent's model.

        Returns:
            The callback handler passed to the model.
        """
        if self.silent:
            return silent_callback_handler
        else:
            return tts_callback_handler

    def generate_session_id(self):
        """
        Generate a unique session ID for this agent.

        Returns:
            A string representing the session ID.
        """
        return f"bbo_agent {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}"

    def set_session_manager(self):
        """
        Return the session manager for this agent.
        If no session manager is provided, it defaults to None.

        Args:
            session_manager: Optional session manager instance.

        Returns:
            The session manager instance or None.
        """
        if self.session_manager is None:
            storage_path = Path(__file__).parent.parent.parent / "data" / "sessions"
            path_to_sessions = (
                Path(__file__).parent.parent.parent
                / "data"
                / "sessions"
                / "session_ids.json"
            )
            with open(path_to_sessions) as f:
                try:
                    sessions = json.load(f)
                except json.JSONDecodeError:
                    logger.warning(
                        "Session IDs file is empty or corrupted. Creating a new one."
                    )
                    sessions = []

            sessions.append(
                {"session_id": self.session_id, "description": "No description yet"}
            )

            with open(path_to_sessions, "w") as f:
                json.dump(sessions, f, indent=2)
            return FileSessionManager(
                session_id=self.session_id, storage_dir=storage_path
            )
        return self.session_manager

    def query(self, question):
        path_to_sessions = (
            Path(__file__).parent.parent.parent
            / "data"
            / "sessions"
            / "session_ids.json"
        )

        with open(path_to_sessions) as f:
            sessions = json.load(f)

        try:
            for session in sessions:
                if session["session_id"] == self.session_id:
                    if session["description"] == "No description yet":
                        session["description"] = question
                        break

            with open(path_to_sessions, "w") as f:
                json.dump(sessions, f, indent=2)

        except Exception as e:
            logger.error(f"An error occurred while updating session description: {e}")
            return f"Error retrieving session description: {e}"

        return super().query(question)

    def get_session_id(self):
        """
        Return the session ID for this agent.

        Returns:
            The session ID string.
        """
        return self.session_id
