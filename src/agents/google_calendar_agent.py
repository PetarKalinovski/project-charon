import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.tools.celander_tools import create_event, get_events
from src.utils.prompts import CALENDAR_AGENT_PROMPT
from src.agents.agent import AgentAbstract
from src.utils.callback_hanlder_subagents import calendar_agent_callback

load_dotenv()


class CalendarAgent(AgentAbstract):
    """
    Main class to run the Google Calendar agent.
    It initializes the agent with the necessary tools and configurations,
    and starts an interactive loop for user commands.
    """

    def get_agent_config(self):
        """Return the Google Calendar agent configuration."""
        return self.config.calendar_agent

    def get_prompt(self):
        """Return the system prompt for this agent."""
        return CALENDAR_AGENT_PROMPT

    def get_tools(self):
        return [
            create_event,
            get_events,
        ]

    def pass_callback_handler(self):
        """
        Pass a callback handler to the agent's model.

        Returns:
            The callback handler passed to the model.
        """
        return calendar_agent_callback
