from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.agents.recommender_agent import RecommenderAgent


def main():
    recommender_agent = RecommenderAgent()
    recommender_agent.query(
        "What recent youtube videos are available from the channels I monitor?"
    )


if __name__ == "__main__":
    main()
