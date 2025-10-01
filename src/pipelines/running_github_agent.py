from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.agents.github_agent import GitHubAgent


def main():
    """
    Main function to run the GitHub agent.
    It initializes the agent with the necessary tools and configurations,
    and starts an interactive loop for user commands.
    """
    github_agent = GitHubAgent()

    print("Welcome to the GitHub Agent!")
    print("You can ask me to manage your repositories, issues, and pull requests.")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = github_agent.query(user_input)
        print(
            f"Agent: {response.message if hasattr(response, 'message') else response}"
        )


if __name__ == "__main__":
    main()
