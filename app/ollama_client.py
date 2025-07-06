import requests
import os

class OllamaClient:
    def __init__(self, model="tinyllama"):
        # Use environment variable for Ollama URL, fallback to localhost
        self.base_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
        self.model = model

    def chat(self, message, system_prompt=None):
        payload = {
            "model": self.model,
            "messages": []
        }
        if system_prompt:
            payload["messages"].append({"role": "system", "content": system_prompt})
        payload["messages"].append({"role": "user", "content": message})

        response = requests.post(f"{self.base_url}/v1/chat/completions", json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}" 