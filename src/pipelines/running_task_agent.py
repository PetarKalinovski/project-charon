import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from agents.task_agent import TaskAgent


def main():
    agent = TaskAgent()

    agent.query(
        "I need to implement a file writting tool in my project called Charon. The project is on github. How long would it take, and look at my calendar to see when you can implement it"
    )


if __name__ == "__main__":
    main()
