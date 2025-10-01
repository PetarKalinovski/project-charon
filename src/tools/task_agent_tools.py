import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.parent)
from strands import tool

from agents.file_search_agent import FileSearchAgent
from agents.google_calendar_agent import CalendarAgent
from agents.github_agent import GitHubAgent
from utils.callback_hanlder_subagents import log_to_session


@tool(
    name="file_search_agent_query",
    description="Query the file search agent to find and analyze files in a project. Useful for understanding project structure, finding specific files, or analyzing code for implementation tasks.",
)
def file_search_agent_query(question: str) -> str:
    """
    Query the file search agent with a specific question about files or project structure.

    Args:
        question (str): The question to ask the file search agent. Examples:
                       - "For the project called Charon, how long would it take me to implement a file writing tool?"
                       - "What files in the CleanEnergy project handle data processing?"
                       - "Show me the structure of the authentication module"

    Returns:
        Union[str, Dict[str, Any]]: The agent's response, which could be a string or structured output
    """
    log_to_session(f"Querying file search agent with question: {question}")

    try:
        agent = FileSearchAgent()
        response = agent.query(question)
        log_to_session("File search agent query completed successfully")
        return response

    except Exception as e:
        error_msg = f"Error querying file search agent: {str(e)}"
        log_to_session(error_msg)
        return error_msg


@tool(
    name="google_calendar_agent_query",
    description="Query the Google Calendar agent to manage calendar events. Can retrieve events, create new events, and provide scheduling assistance.",
)
def google_calendar_agent_query(query: str) -> str:
    """
    Query the Google Calendar agent with a calendar-related request.

    Args:
        query (str): The calendar-related query. Examples:
                    - "What events do I have today?"
                    - "Create a meeting for tomorrow at 2 PM"
                    - "Show me my schedule for the next 3 days"
                    - "When am I free this week?"

    Returns:
        str: The agent's response regarding calendar operations
    """
    try:
        log_to_session(f"Querying calendar agent with: {query}")
        agent = CalendarAgent()
        response = agent.query(query)
        log_to_session("Calendar agent query completed successfully")
        return str(response)
    except Exception as e:
        error_msg = f"Error querying calendar agent: {str(e)}"
        log_to_session(error_msg)
        return error_msg


@tool(
    name="github_agent_query",
    description="Query the GitHub agent to manage GitHub repositories and issues. Can retrieve repository information, create issues, and manage pull requests.",
)
def github_agent_query(query: str) -> str:
    """
    Query the GitHub agent with a GitHub-related request.

    Args:
        query (str): The GitHub-related query. Examples:
                    - "What issues are open in my repository?"
                    - "Create a new issue for bug #123"
                    - "Show me the pull requests in my repository"
                    - "How do I clone my repository?"

    Returns:
        str: The agent's response regarding GitHub operations
    """
    try:
        log_to_session(f"Querying GitHub agent with: {query}")
        agent = GitHubAgent()
        response = agent.query(query)
        log_to_session("GitHub agent query completed successfully")
        return str(response)
    except Exception as e:
        error_msg = f"Error querying GitHub agent: {str(e)}"
        log_to_session(error_msg)
        return error_msg
