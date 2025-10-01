import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from agents.file_search_agent import FileSearchAgent


def main():
    """
    Main function to run the file search agent.
    It initializes the agent with the necessary tools and configurations,
    and starts an interactive loop for user commands.
    """

    agent = FileSearchAgent()

    agent.query(
        "For the project called Charon, how long would it take me to implement a file writting tool?"
    )

    # print(find_folder_from_name("project-charon"))


if __name__ == "__main__":
    main()
