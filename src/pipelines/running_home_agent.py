from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.agents.home_agent import HomeAgent


def main():
    home_agent = HomeAgent()
    home_agent.query("Find me a youtube video I can watch between meetings today.")


if __name__ == "__main__":
    main()
