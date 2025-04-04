import requests
import json

url = "http://localhost:11434/api/generate"

payload = {
    "model": "llama3.2",
    "prompt": "Why is the sky blue?",
    "stream": True
}

response = requests.post(url, json=payload, stream=True)

for line in response.iter_lines():
    if line:
        try:
            chunk = json.loads(line)
            print(chunk.get("response", ""), end="", flush=True)
        except json.JSONDecodeError as e:
            print(f"\n[JSON error: {e}]")
