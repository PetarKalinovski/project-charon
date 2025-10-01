from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.tools.movies_tools import (
    add_movie_or_show_to_watchlist,
    get_movies_and_show_list,
    mark_movie_or_show_watched,
    search_omdb_movie_or_show,
)
from src.agents.agent import AgentAbstract
from dotenv import load_dotenv
from utils.prompts import MOVIES_AGENT_PROMPT
from src.utils.callback_hanlder_subagents import movie_agent_callback

load_dotenv()


class MoviesAgent(AgentAbstract):
    """
    A movies agent that can manage tasks related to movies and shows.
    It can add movies or shows to a watchlist, mark them as watched, and search for them.
    """

    def get_agent_config(self):
        """Return the Movies agent configuration."""
        return self.config.movies_agent

    def get_prompt(self):
        """Return the system prompt for this agent."""
        return MOVIES_AGENT_PROMPT

    def get_tools(self):
        """Return the list of tools available for this agent."""
        return [
            add_movie_or_show_to_watchlist,
            get_movies_and_show_list,
            mark_movie_or_show_watched,
            search_omdb_movie_or_show,
        ]

    def pass_callback_handler(self):
        """
        Pass a callback handler to the agent's model.

        Returns:
            The callback handler passed to the model.
        """
        return movie_agent_callback
