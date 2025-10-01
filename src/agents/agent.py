import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.models import BedrockModel
from strands.models.litellm import LiteLLMModel

sys.path.append(str(Path(__file__).parent.parent))
from typing import Optional

from src.utils.config_loader import load_config

from abc import ABC, abstractmethod

load_dotenv()


class AgentAbstract(ABC):
    """Abstract base class for agents that can be initialized with different model configurations
    and provides methods for running queries"""

    def __init__(self, config: Optional[object] = None):
        """
        Initialize the agent with the necessary tools and configurations.

        Args:
            config: Optional configuration object. If None, will load from load_config()
        """
        self.config = config or load_config()
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.model_id = self.get_agent_config().model.model_id
        self.callback_handler = self.pass_callback_handler() or None
        self.model = self._initialize_model()
        self.agent = self._initialize_agent()

    @abstractmethod
    def get_agent_config(self):
        """
        Return the specific configuration section for this agent.

        Returns:
            The configuration object for this specific agent
        """
        pass

    @abstractmethod
    def get_prompt(self):
        """
        Return the system prompt for this agent.

        Returns:
            The system prompt string for this specific agent
        """
        pass

    @abstractmethod
    def get_tools(self):
        """
        Return the tools available to this agent.

        Returns:
            A list of tool names or identifiers
        """
        pass

    def pass_callback_handler(self):
        """
        Pass a callback handler to the agent's model.

        Args:
            callback_handler: The callback handler to be used by the model.
        Returns:
            The callback handler passed to the model.
        """
        pass

    def _initialize_model(self):
        """Initialize the appropriate model based on configuration."""
        if self.model_id.startswith("openrouter"):
            return LiteLLMModel(
                model_id=self.model_id,
                client_args={"api_key": self.openrouter_api_key},
                max_tokens=10000,
                streaming=True,
            )
        elif "anthropic" in self.model_id:
            return BedrockModel(
                model_id=self.model_id,
                client_args={"region_name": "us-east-1"},
            )
        else:
            raise ValueError(f"Unsupported model type: {self.model_id}")

    def set_session_manager(self):
        """
        Return the session manager for this agent.
        """
        return None

    def _initialize_agent(self):
        """Initialize the agent with tools, model, and conversation manager."""
        tools = self.get_tools()
        session_manager = self.set_session_manager()

        if self.callback_handler:
            self.agent = Agent(
                model=self.model,
                tools=tools,
                conversation_manager=SlidingWindowConversationManager(window_size=10),
                system_prompt=self.get_prompt(),
                callback_handler=self.callback_handler,
                session_manager=session_manager if session_manager else None,
            )
        else:
            self.agent = Agent(
                model=self.model,
                tools=tools,
                conversation_manager=SlidingWindowConversationManager(window_size=10),
                system_prompt=self.get_prompt(),
            )

        return self.agent

    def query(self, question: str):
        """
        Run a single query against the agent.

        Args:
            question: The question to ask the agent

        Returns:
            The agent's response
        """
        return self.agent(question)
