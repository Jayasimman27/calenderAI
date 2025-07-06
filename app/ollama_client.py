import requests
import os

class OllamaClient:
    def __init__(self, model="tinyllama"):
        # Use environment variable for Ollama URL, fallback to localhost
        self.base_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
        self.model = model

    def chat(self, message, system_prompt=None):
        try:
            payload = {
                "model": self.model,
                "messages": []
            }
            if system_prompt:
                payload["messages"].append({"role": "system", "content": system_prompt})
            payload["messages"].append({"role": "user", "content": message})

            response = requests.post(f"{self.base_url}/v1/chat/completions", json=payload, timeout=10)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return self._get_fallback_response(message)
        except Exception as e:
            return self._get_fallback_response(message)
    
    def _get_fallback_response(self, message):
        """Provide fallback responses when Ollama is not available"""
        message_lower = message.lower()
        
        if "hello" in message_lower or "hi" in message_lower:
            return "Hello! I'm TailorTalk, your AI calendar assistant. I can help you manage your Google Calendar events."
        elif "help" in message_lower:
            return "I can help you with calendar tasks! Try asking me to 'create a meeting at 3 PM today for team standup' or 'show my events'."
        elif "calendar" in message_lower or "event" in message_lower:
            return "I'm here to help with your calendar! You can ask me to create events, show your schedule, or manage your meetings."
        else:
            return "I'm TailorTalk, your AI calendar assistant. I can help you create, view, and manage your Google Calendar events. Try asking me to create a meeting or show your events!" 