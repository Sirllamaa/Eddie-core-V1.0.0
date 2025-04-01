import os
import subprocess
import sys
import contextlib
from typing import Tuple
from llama_cpp import Llama
import openai
import anthropic


def is_online() -> bool:
    return subprocess.call("ping -c 1 -W 1 8.8.8.8", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

tinyllama_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "tinyllama.gguf"))

router_model = Llama(model_path=tinyllama_path, n_ctx=2048, n_threads=4, verbose=False)

openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
anthropic_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))


def select_model(user_input: str) -> str:
    prompt = (
        "Classify the user's intent based on the following criteria. For each, score from 1 (very low) to 10 (very high):\n"
        "- Logic Complexity: Does the task require logical thinking?\n"
        "- Math Involvement: Are math skills required?\n"
        "- Reasoning Depth: Does it need multi-step inference?\n"
        "- Creativity: Is it imaginative or generative?\n"
        "- Triviality: Is it overly simple or obvious? (10 = very trivial)\n\n"
        f'User input: "{user_input}"\n\n'
        "Respond in this format:\n"
        "Logic Complexity: #\n"
        "Math Involvement: #\n"
        "Reasoning Depth: #\n"
        "Creativity: #\n"
        "Triviality: #"
    )

    result = router_model(prompt, max_tokens=128, temperature=0.2)

    try:
        return result["choices"][0]["text"].strip()
    except (KeyError, IndexError):
        return "<No response>"

if __name__ == '__main__':
    output = select_model("Turn on the light.")
    print(f"[Model Output] {output}")

