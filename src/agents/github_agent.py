from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters
from dotenv import load_dotenv
import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from src.utils.prompts import GITHUB_AGENT_PROMPT
from src.agents.agent import AgentAbstract  # Import your abstract base class
from src.utils.callback_hanlder_subagents import github_agent_callback

load_dotenv()


class GitHubAgent(AgentAbstract):
    """
    A GitHub agent that can interact with GitHub repositories using the Model Context Protocol (MCP).
    It can list repositories and fetch README files from the most recent project.
    """

    def __init__(self, config=None):
        # Initialize GitHub-specific attributes before calling super()
        self.api_key = os.getenv("GITHUB_TOKEN")
        self.github_client = self._initialize_github_client()

        # Call parent constructor
        super().__init__(config)

    def get_agent_config(self):
        """Return the GitHub agent configuration."""
        return self.config.github_agent

    def get_tools(self):
        """
        Return the list of tools from the MCP client.
        Note: This returns an empty list since tools are loaded dynamically in query().
        """
        return []

    def get_prompt(self):
        """Return the GitHub agent system prompt."""
        return GITHUB_AGENT_PROMPT

    def _initialize_github_client(self):
        """Initialize the GitHub client using MCP."""
        return MCPClient(
            lambda: stdio_client(
                StdioServerParameters(
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-github"],
                    env={"GITHUB_PERSONAL_ACCESS_TOKEN": self.api_key},
                )
            )
        )

    def query(self, user_input: str):
        """
        Run the agent with the provided user input.
        This method overrides the parent's query method to handle MCP client context.
        """
        with self.github_client:
            agent = Agent(
                model=self.model,
                tools=self.github_client.list_tools_sync(),
                system_prompt=self.get_prompt(),
            )
            response = agent(user_input)
            return response

    def pass_callback_handler(self):
        """
        Pass a callback handler to the agent's model.

        Returns:
            The callback handler passed to the model.
        """
        return github_agent_callback
