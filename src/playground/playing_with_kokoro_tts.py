from kokoro import KPipeline
import sounddevice as sd
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.agents.big_boss_orchestrator_agent import BigBossOrchestratorAgent


def main():
    # Load your model and tokenizer here
    pipeline = KPipeline(lang_code="a")

    bm_lewis = pipeline.load_voice("bm_lewis")

    am_michael = pipeline.load_voice("am_michael")

    blend = np.add(bm_lewis * 0.8, am_michael * 0.2)

    agent = BigBossOrchestratorAgent()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = agent.query(user_input)

        print(f"Agent: {response}")

        print(f"Response.message => {response.message}")

        generator = pipeline(
            response.message, voice=blend, speed=1.0, split_pattern=r"\n+"
        )

        for i, (gs, ps, audio) in enumerate(generator):
            print(i)  # i => index
            print(gs)  # gs => graphemes/text
            print(ps)  # ps => phonemes
            # Save audio to file
            # sf.write(f"output_{i}.wav", audio, 24000)
            sd.play(audio, 24000)
            sd.wait()


if __name__ == "__main__":
    main()
