from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.agents.agent import AgentAbstract
from src.tools.home_agent_tools import (
    book_agent_query,
    movies_agent_query,
    recommender_agent_query,
)
from src.tools.celander_tools import get_events, create_event
from src.utils.prompts import HOME_AGENT_PROMPT
from src.utils.callback_hanlder_subagents import home_agent_callback


class HomeAgent(AgentAbstract):
    """
    HomeAgent is responsible for managing home-related tasks such as querying book and movie agents,
    and handling recommendations.
    """

    def get_agent_config(self):
        """Return the Home agent configuration."""
        return self.config.home_agent

    def get_prompt(self):
        """Return the system prompt for this agent."""
        return HOME_AGENT_PROMPT

    def get_tools(self):
        """Return the list of tools available for this agent."""
        return [
            book_agent_query,
            movies_agent_query,
            recommender_agent_query,
            get_events,
            create_event,
        ]

    def pass_callback_handler(self):
        """
        Pass a callback handler to the agent's model.

        Returns:
            The callback handler passed to the model.
        """
        return home_agent_callback
