from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from src.tools.recommender_agent_tools import (
    add_substack_newsletter_to_monitor,
    get_all_newsletters,
    get_recent_posts_from_newsletter,
    get_recent_youtube_videos,
    get_all_monitored_youtube_channels,
    add_youtube_channel_to_monitor,
)
from src.agents.agent import AgentAbstract
from dotenv import load_dotenv
from src.utils.prompts import RECOMMENDER_AGENT_PROMPT
from src.utils.callback_hanlder_subagents import recommender_agent_callback

load_dotenv()


class RecommenderAgent(AgentAbstract):
    """
    A recommender agent that can manage tasks related to newsletters and YouTube channels.
    It can add newsletters and channels to a monitoring list, retrieve metadata, and get recent videos.
    """

    def get_agent_config(self):
        """Return the Recommender agent configuration."""
        return self.config.recommender_agent

    def get_prompt(self):
        """Return the system prompt for this agent."""
        return RECOMMENDER_AGENT_PROMPT

    def get_tools(self):
        """Return the list of tools available for this agent."""
        return [
            add_substack_newsletter_to_monitor,
            get_all_newsletters,
            get_recent_posts_from_newsletter,
            get_recent_youtube_videos,
            get_all_monitored_youtube_channels,
            add_youtube_channel_to_monitor,
        ]

    def pass_callback_handler(self):
        """
        Pass a callback handler to the agent's model.

        Returns:
            The callback handler passed to the model.
        """
        return recommender_agent_callback
