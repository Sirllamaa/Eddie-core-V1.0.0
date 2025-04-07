import requests
import os
from config import OPENAI_API_KEY

OPENAI_API_KEY = OPENAI_API_KEY

def extract_memory_from_llm(user_input: str, assistant_response: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set in the environment")

    full_convo = f"User: {user_input}\nAssistant: {assistant_response}"

    system_message = (
        "You are a memory extraction tool. Your ONLY task is to extract factual information about the user. "
        "Respond ONLY with a sentence or two describing what the user said about themselves, in third person. "
        "DO NOT greet, ask questions, or act like a chat assistant. Do not include anything unrelated to facts. "
        "Example response: 'The user recently got a golden retriever named Max.' "
        "If you believe there is nothing worthy of remembering, respond with 'Nothing to remember.'"
    )

    payload = {
        "model": "gpt-4o",
        "messages": [
            { "role": "system", "content": system_message },
            { "role": "user", "content": full_convo }
        ],
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        raise RuntimeError(f"Memory extraction failed: {e}")
