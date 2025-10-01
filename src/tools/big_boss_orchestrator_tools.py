from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.agents.task_agent import TaskAgent
from src.agents.home_agent import HomeAgent
from strands import tool
from loguru import logger


@tool
def task_agent_query(query: str) -> str:
    """
    Query the Task Agent with a specific query.

    Args:
        query (str): The query to send to the Task Agent.

    Returns:
        str: The response from the Task Agent.
    """
    try:
        agent = TaskAgent()
        response = agent.query(query)
        logger.success("Task Agent responded successfully.")

        return response
    except Exception as e:
        logger.error(f"An error occurred while querying the Task Agent: {str(e)}")
        return f"An error occurred while querying the Task Agent: {str(e)}"


@tool
def home_agent_query(query: str) -> str:
    """
    Query the Home Agent with a specific query.

    Args:
        query (str): The query to send to the Home Agent.

    Returns:
        str: The response from the Home Agent.
    """
    try:
        agent = HomeAgent()
        response = agent.query(query)
        logger.success("Home Agent responded successfully.")
        return response
    except Exception as e:
        logger.error(f"An error occurred while querying the Home Agent: {str(e)}")
        return f"An error occurred while querying the Home Agent: {str(e)}"
