from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.agents.big_boss_orchestrator_agent import BigBossOrchestratorAgent


def main():
    """
    Main function to run the Big Boss Orchestrator Agent.
    This function initializes the agent and starts the orchestration process.
    """
    agent = BigBossOrchestratorAgent()
    # Here you can add code to start the agent or perform specific tasks
    print("Big Boss Orchestrator Agent is ready to orchestrate tasks.")

    while True:
        user_input = input(
            "Enter a command for the Big Boss Orchestrator Agent (or 'exit' to quit): "
        )
        if user_input.lower() == "exit":
            print("Exiting the Big Boss Orchestrator Agent.")
            break
        response = agent.query(user_input)
        print(f"Agent Response: {response}")


if __name__ == "__main__":
    main()
