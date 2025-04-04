import requests
import json

OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "llama3.1:latest"

# Conversation history – you can append to this across turns
chat_history = []

def chat_with_llama(user_message: str, system_prompt: str = None):
    headers = {"Content-Type": "application/json"}

    # Build message list
    messages = []
    if system_prompt:
        messages.append({ "role": "system", "content": system_prompt })

    messages.extend(chat_history)
    messages.append({ "role": "user", "content": user_message })

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": True
    }

    # Send request with streaming
    with requests.post(f"{OLLAMA_HOST}/api/chat", json=payload, headers=headers, stream=True) as response:
        response.raise_for_status()
        print("Assistant: ", end="", flush=True)
        full_response = ""
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                delta = chunk.get("message", {}).get("content", "")
                print(delta, end="", flush=True)
                full_response += delta

    # Save the assistant reply to history
    chat_history.append({ "role": "user", "content": user_message })
    chat_history.append({ "role": "assistant", "content": full_response })


if __name__ == "__main__":
    system_prompt = "You are a helpful assistant."

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        chat_with_llama(user_input, system_prompt)
