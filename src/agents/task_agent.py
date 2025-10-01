import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

from src.tools.task_agent_tools import (
    file_search_agent_query,
    google_calendar_agent_query,
    github_agent_query,
)
from src.agents.agent import AgentAbstract
from src.utils.prompts import TASK_AGENT_PROMPT
from src.utils.callback_hanlder_subagents import task_agent_callback

load_dotenv()


class TaskAgent(AgentAbstract):
    """
    A main agent that can delegate tasks to specialized sub-agents.
    This agent can handle both file/project analysis and calendar management.
    """

    def get_agent_config(self):
        """Return the Task agent configuration."""
        return self.config.task_agent

    def get_prompt(self):
        """Return the system prompt for this agent."""
        return TASK_AGENT_PROMPT

    def get_tools(self):
        """Return the list of tools available for this agent."""
        return [
            file_search_agent_query,
            google_calendar_agent_query,
            github_agent_query,
        ]

    def pass_callback_handler(self):
        """
        Pass a callback handler to the agent's model.

        Returns:
            The callback handler passed to the model.
        """
        return task_agent_callback
