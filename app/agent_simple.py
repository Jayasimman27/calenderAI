import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import requests
import json

from .calendar_utils import GoogleCalendarManager
from .models import ChatMessage, ChatResponse

class SimpleTailorTalkAgent:
    def __init__(self):
        """
        Initialize a simplified TailorTalk agent without LangChain
        """
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.calendar_manager = GoogleCalendarManager()
        
        if not self.openai_api_key:
            print("Warning: OPENAI_API_KEY not found. Some features may not work.")
    
    async def process_message(self, message: str) -> str:
        """
        Process a user message using OpenAI API directly
        """
        if not self.openai_api_key:
            return "Error: OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        
        try:
            # Simple prompt for calendar management
            system_prompt = """You are TailorTalk, a helpful AI assistant that manages Google Calendar events. 
            You can help users:
            - Show upcoming events
            - Create new events
            - Delete events
            - Update events
            
            Respond naturally and helpfully. If the user wants to manage calendar events, 
            provide clear instructions on what information you need."""
            
            # Call OpenAI API directly
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Error calling OpenAI API: {response.status_code}"
                
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    def get_calendar_events(self) -> List[Dict[str, Any]]:
        """
        Get calendar events for API endpoint
        """
        return self.calendar_manager.get_upcoming_events()
    
    def create_calendar_event(self, summary: str, start_time: str, end_time: str, 
                            description: str = "", location: str = "") -> Dict[str, Any]:
        """
        Create a new calendar event
        """
        return self.calendar_manager.create_event(summary, start_time, end_time, description, location)
    
    def delete_calendar_event(self, event_id: str) -> bool:
        """
        Delete a calendar event
        """
        return self.calendar_manager.delete_event(event_id)
    
    def update_calendar_event(self, event_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update an existing calendar event
        """
        return self.calendar_manager.update_event(event_id, **kwargs) 