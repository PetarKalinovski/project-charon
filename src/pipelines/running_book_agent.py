from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from agents.books_agent import BookAgent


def main():
    while True:
        book_agent = BookAgent()
        user_query = input("Enter your query for the Book Agent (or 'exit' to quit): ")
        if user_query.lower() == "exit":
            break
        response = book_agent.query(user_query)
        print(f"Response from Book Agent: {response}")


if __name__ == "__main__":
    main()
