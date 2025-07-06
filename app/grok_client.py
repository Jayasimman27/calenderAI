import os
import requests
from typing import Optional, Dict, Any
from pydantic import BaseModel

class GrokClient:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Grok API client
        """
        self.api_key = api_key or os.getenv("GROK_API_KEY")
        self.base_url = "https://api.x.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(self, messages: list, model: str = "grok") -> str:
        """
        Send a chat completion request to Grok API
        """
        if not self.api_key:
            return "Error: Grok API key not configured. Please set GROK_API_KEY environment variable."
        
        try:
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Grok API: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def simple_chat(self, message: str, system_prompt: str = None) -> str:
        """
        Simple chat interface
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": message})
        
        return self.chat_completion(messages) 