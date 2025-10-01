from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.callback_hanlder_subagents import log_to_session
from agents.books_agent import BookAgent
from agents.movies_agent import MoviesAgent
from agents.recommender_agent import RecommenderAgent
from strands import tool


@tool
def book_agent_query(query: str) -> str:
    """
    Query the Book Agent with a specific request.
    Args:
        query (str): The query to send to the Book Agent.
    Returns:
        str: The response from the Book Agent.
    """

    try:
        agent = BookAgent()
        response = agent.query(query)
        log_to_session("Book Agent responded successfully.")
        return response
    except Exception as e:
        log_to_session(f"An error occurred while querying the Book Agent: {str(e)}")
        return f"An error occurred while querying the Book Agent: {str(e)}"


@tool
def movies_agent_query(query: str) -> str:
    """
    Query the Movies Agent with a specific request.
    Args:
        query (str): The query to send to the Movies Agent.
    Returns:
        str: The response from the Movies Agent.
    """

    try:
        agent = MoviesAgent()
        response = agent.query(query)
        log_to_session("Movies Agent responded successfully.")
        return response
    except Exception as e:
        log_to_session(f"An error occurred while querying the Movies Agent: {str(e)}")
        return f"An error occurred while querying the Movies Agent: {str(e)}"


@tool
def recommender_agent_query(query: str) -> str:
    """
    Query the Recommender Agent with a specific request.
    Args:
        query (str): The query to send to the Recommender Agent.
    Returns:
        str: The response from the Recommender Agent.
    """
    try:
        agent = RecommenderAgent()
        response = agent.query(query)
        log_to_session("Recommender Agent responded successfully.")
        return response
    except Exception as e:
        log_to_session(
            f"An error occurred while querying the Recommender Agent: {str(e)}"
        )
        return f"An error occurred while querying the Recommender Agent: {str(e)}"
