import requests
from typing import List, Optional, Literal
from datetime import datetime
import uuid
import logging
from config import SYSTEM_API_KEY

class EmbeddingGenerator:
    def __init__(self,
                 mode: Literal["local"] = "local",
                 model_name: str = "nomic-embed-text",
                 ollama_url: str = "http://localhost:11434/api/embeddings",
                 eddie_store_url: str = "http://127.0.0.1:8001/store/api/v1/memory/add",  # Adjust if hosted elsewhere
                 token: Optional[str] = None):
        self.mode = mode
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.eddie_store_url = eddie_store_url
        self.token = token

        if mode != "local":
            raise ValueError("Only 'local' mode is currently supported.")

    def generate(self, text: str) -> List[float]:
        """Generate embedding for a given text using local Ollama."""
        if self.mode == "local":
            return self._generate_local(text)
        else:
            raise NotImplementedError("Cloud embedding not implemented yet.")

    def _generate_local(self, text: str) -> List[float]:
        payload = {
            "model": self.model_name,
            "prompt": text,
        }

        try:
            response = requests.post(self.ollama_url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["embedding"]
        except Exception as e:
            logging.error(f"Failed to get embedding from Ollama: {e}")
            raise

    def send_to_eddie_store(self, text: str, embedding: List[float], metadata: Optional[dict] = None) -> dict:
        """Send the embedding and original text to Eddie Store."""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        if metadata is None:
            metadata = {}

        metadata["timestamp"] = datetime.utcnow().isoformat()

        payload = {
            "text": text,
            "embedding": embedding,
            "metadata": metadata
        }

        try:
            response = requests.post(self.eddie_store_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Failed to send to Eddie Store: {e}")
            raise

if __name__ == "__main__":
    token = SYSTEM_API_KEY
    
    generator = EmbeddingGenerator(token=token)

    text = "Eddie is a privacy-first personal assistant."
    embedding = generator.generate(text)

    result = generator.send_to_eddie_store(text, embedding)
    print("Memory added:", result)
