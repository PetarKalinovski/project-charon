from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from agents.movies_agent import MoviesAgent


def main():
    """
    Main function to run the Movies Agent.
    It initializes the agent with the necessary tools and configurations,
    and starts an interactive loop for user commands.
    """
    movies_agent = MoviesAgent()

    print("Welcome to the Movies Agent!")
    print("You can ask me to manage your movies and shows.")
    print("Type 'exit' to quit.")

    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower() == "exit":
    #         break

    #     response = movies_agent.agent(user_input)
    #     print(
    #         f"Agent: {response.message if hasattr(response, 'message') else response}"
    #     )

    movies_agent.query(
        "I have watched Dune: part 2 and I want to add it to my watched section. I will give it a rating of 9.5 and I want to add a note that it was an amazing movie with stunning visuals and a great soundtrack."
    )


if __name__ == "__main__":
    main()
