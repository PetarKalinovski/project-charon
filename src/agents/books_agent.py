from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.tools.books_tools import (
    add_book_to_reading_list,
    get_book_lists,
    mark_book_read,
    search_book,
)
from src.agents.agent import AgentAbstract
from dotenv import load_dotenv
from src.utils.prompts import BOOKS_AGENT_PROMPT
from src.utils.callback_hanlder_subagents import book_agent_callback

load_dotenv()


class BookAgent(AgentAbstract):
    """
    A book agent that can manage tasks related to books.
    It can add books to a reading list, mark books as read, and search for books.
    """

    def get_agent_config(self):
        """Return the Books agent configuration."""
        return self.config.books_agent

    def get_prompt(self):
        """Return the system prompt for this agent."""
        return BOOKS_AGENT_PROMPT

    def get_tools(self):
        """Return the list of tools available for this agent."""
        return [
            add_book_to_reading_list,
            get_book_lists,
            mark_book_read,
            search_book,
        ]

    def pass_callback_handler(self):
        """
        Pass a callback handler to the agent's model.

        Returns:
            The callback handler passed to the model.
        """
        return book_agent_callback
