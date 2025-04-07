import requests

def extract_memory_from_llm(user_input: str, assistant_response: str) -> str:
    full_convo = f"User: {user_input}\nAssistant: {assistant_response}"
    system_message = (
         "You are a memory extraction tool. Your ONLY task is to extract factual information about the user. "
    "Respond ONLY with a sentence or two describing what the user said about themselves, in third person. "
    "DO NOT greet, ask questions, or act like a chat assistant. Do not include anything unrelated to facts. "
    "Example response: 'The user recently got a golden retriever named Max.'"
    "If you belive there is nothing worthy of remembering, respond with 'Nothing to remember.'"
    )

    payload = {
        "model": "llama3:latest",
        "system": system_message,
        "messages": [{"role": "user", "content": system_message + full_convo}],
        "stream": False
    }

    try:
        res = requests.post("http://localhost:11434/api/chat", json=payload)
        res.raise_for_status()
        return res.json()["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Memory extraction failed: {e}")
