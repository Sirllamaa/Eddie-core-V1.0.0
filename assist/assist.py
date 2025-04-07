import requests
import json
import os
from config import OPENAI_API_KEY

# Default configs
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama3:latest"
OPENAI_MODEL = "gpt-4o"
OPENAI_API_KEY = OPENAI_API_KEY

# Shared conversation history (can later be made per-user)
chat_history = []

def query_llm(user_message: str, system_prompt: str = None, backend: str = "openai") -> str:
    if backend == "openai":
        return query_openai(user_message, system_prompt)
    elif backend == "ollama":
        return query_ollama(user_message, system_prompt)
    else:
        raise ValueError("Unsupported backend: choose 'ollama' or 'openai'")

def query_ollama(user_message: str, system_prompt: str = None) -> str:
    headers = {"Content-Type": "application/json"}

    messages = []
    if system_prompt:
        messages.append({ "role": "system", "content": system_prompt })

    messages.extend(chat_history)
    messages.append({ "role": "user", "content": user_message })

    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    }

    with requests.post(f"{OLLAMA_HOST}/api/chat", json=payload, headers=headers, stream=True) as response:
        response.raise_for_status()
        full_response = ""
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                delta = chunk.get("message", {}).get("content", "")
                full_response += delta

    chat_history.append({ "role": "user", "content": user_message })
    chat_history.append({ "role": "assistant", "content": full_response })

    return full_response.strip()

def query_openai(user_message: str, system_prompt: str = None) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = []
    if system_prompt:
        messages.append({ "role": "system", "content": system_prompt })

    messages.extend(chat_history)
    messages.append({ "role": "user", "content": user_message })

    payload = {
        "model": OPENAI_MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()["choices"][0]["message"]["content"]

    chat_history.append({ "role": "user", "content": user_message })
    chat_history.append({ "role": "assistant", "content": result })

    return result.strip()

# Example usage
if __name__ == "__main__":
    system = "You are a helpful assistant."
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        reply = query_llm(user_input, system_prompt=system, backend="openai")  # or "ollama"
        print("Assistant:", reply)
