import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from agents.google_calendar_agent import CalendarAgent


def main():
    """
    Main function to run the Google Calendar agent.
    It initializes the agent with the necessary tools and configurations,
    """
    calendar_agent = CalendarAgent()

    print("Welcome to the Google Calendar Agent!")
    print("You can ask me to retrieve events or create new events.")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = calendar_agent.query(user_input)
        print(
            f"Agent: {response.message if hasattr(response, 'message') else response}"
        )


if __name__ == "__main__":
    main()
