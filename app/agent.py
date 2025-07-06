import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import re

from .calendar_utils import GoogleCalendarManager
from .models import ChatMessage, ChatResponse
from .ollama_client import OllamaClient

class TailorTalkAgent:
    def __init__(self):
        """
        Initialize the TailorTalk agent with Ollama LLM
        """
        # Use Ollama LLM
        self.ollama_client = OllamaClient(model="tinyllama")
        
        # Initialize calendar manager
        self.calendar_manager = GoogleCalendarManager()
        
        # Initialize simple memory for chat history
        self.chat_history = []
    

    

    
    async def process_message(self, message: str) -> str:
        """
        Process a user message and return the agent's response
        """
        try:
            # Check if the message is about calendar operations
            message_lower = message.lower()
            
            # Check for event creation keywords
            event_keywords = ["create", "add", "schedule", "meet", "meeting", "event"]
            time_keywords = ["pm", "am", ":", "today", "tomorrow"]
            
            has_event_keyword = any(keyword in message_lower for keyword in event_keywords)
            has_time_keyword = any(keyword in message_lower for keyword in time_keywords)
            
            if has_event_keyword and has_time_keyword:
                # Extract event details from the message
                response = self._handle_create_event(message)
            elif "show" in message_lower and ("event" in message_lower or "calendar" in message_lower):
                # Show calendar events
                response = self._handle_show_events()
            elif "delete" in message_lower and "event" in message_lower:
                # Handle event deletion
                response = "I can help you delete events. Please provide the event ID or name."
            else:
                # General conversation
                system_prompt = """You are TailorTalk, a helpful AI assistant that can manage Google Calendar events. 
                Keep your responses concise and focused on calendar management tasks. 
                You can help with: viewing events, creating events, updating events, and deleting events."""
                response = self.ollama_client.chat(message, system_prompt)
            
            return response
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    def _handle_create_event(self, message: str) -> str:
        """Handle event creation requests"""
        try:
            from datetime import datetime, timedelta
            import re
            
            message_lower = message.lower()
            
            # Parse the message for event details
            event_title = None
            event_time = None
            event_date = "today"
            
            # Extract event title (look for words after "for" or "called")
            if "for" in message_lower:
                parts = message_lower.split("for")
                if len(parts) > 1:
                    event_title = parts[1].strip()
            elif "called" in message_lower:
                parts = message_lower.split("called")
                if len(parts) > 1:
                    event_title = parts[1].strip()
            
            # Extract time (look for patterns like "4pm", "4 pm", "16:00")
            time_pattern = r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?'
            time_match = re.search(time_pattern, message_lower)
            
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2)) if time_match.group(2) else 0
                ampm = time_match.group(3)
                
                # Convert to 24-hour format
                if ampm == "pm" and hour != 12:
                    hour += 12
                elif ampm == "am" and hour == 12:
                    hour = 0
                
                event_time = f"{hour:02d}:{minute:02d}"
            
            # Determine date
            if "today" in message_lower:
                event_date = "today"
            elif "tomorrow" in message_lower:
                event_date = "tomorrow"
            elif "next" in message_lower and any(day in message_lower for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
                # Handle "next Monday", "next Friday", etc.
                for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                    if day in message_lower:
                        event_date = f"next {day}"
                        break
            elif any(month in message_lower for month in ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]):
                # Handle specific dates like "July 10th"
                event_date = "specific_date"
            
            # Create the event
            if event_title and event_time:
                # Parse the time
                hour, minute = map(int, event_time.split(":"))
                
                # Calculate start time
                now = datetime.utcnow()
                if event_date == "today":
                    start_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                elif event_date == "tomorrow":
                    start_time = (now + timedelta(days=1)).replace(hour=hour, minute=minute, second=0, microsecond=0)
                elif event_date.startswith("next "):
                    # Handle "next Monday", "next Friday", etc.
                    day_name = event_date.split(" ")[1]
                    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                    target_day = days_of_week.index(day_name.lower())
                    current_day = now.weekday()
                    days_ahead = target_day - current_day
                    if days_ahead <= 0:  # Target day has passed this week
                        days_ahead += 7
                    start_time = (now + timedelta(days=days_ahead)).replace(hour=hour, minute=minute, second=0, microsecond=0)
                elif event_date == "specific_date":
                    # For now, default to tomorrow for specific dates
                    # In a full implementation, you'd parse the actual date
                    start_time = (now + timedelta(days=1)).replace(hour=hour, minute=minute, second=0, microsecond=0)
                else:
                    # Default to tomorrow
                    start_time = (now + timedelta(days=1)).replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                # End time (1 hour later by default)
                end_time = start_time + timedelta(hours=1)
                
                # Format for Google Calendar
                start_time_str = start_time.isoformat() + 'Z'
                end_time_str = end_time.isoformat() + 'Z'
                
                # Create the event
                event = self.calendar_manager.create_event(
                    summary=event_title.title(),
                    start_time=start_time_str,
                    end_time=end_time_str,
                    description=f"Event created by TailorTalk: {event_title}"
                )
                
                # Format the response with actual date
                if event_date == "today":
                    date_str = "today"
                elif event_date == "tomorrow":
                    date_str = "tomorrow"
                elif event_date.startswith("next "):
                    date_str = event_date
                else:
                    date_str = event_date
                
                return f"✅ Event created successfully! Title: {event_title.title()}, Time: {event_time} {date_str}"
            else:
                return "I understand you want to create an event. Please provide the event title and time (e.g., 'Create a meeting at 4 PM today for Team Standup')"
                
        except Exception as e:
            return f"Error creating event: {str(e)}"
    
    def _handle_show_events(self) -> str:
        """Handle requests to show calendar events"""
        try:
            events = self.calendar_manager.get_upcoming_events()
            if events:
                event_list = []
                for event in events:
                    event_list.append(f"- {event['summary']} on {event['start']}")
                return f"Here are your upcoming events:\n" + "\n".join(event_list)
            else:
                return "You don't have any upcoming events in your calendar."
        except Exception as e:
            return f"Error getting events: {str(e)}"
    
    def _get_calendar_events(self, query: str = "") -> str:
        """
        Get upcoming calendar events
        """
        try:
            events = self.calendar_manager.get_upcoming_events()
            if not events:
                return "No upcoming events found in your calendar."
            
            event_list = []
            for event in events:
                start_time = datetime.fromisoformat(event['start'].replace('Z', '+00:00'))
                formatted_time = start_time.strftime("%Y-%m-%d %H:%M")
                event_list.append(f"- {event['summary']} on {formatted_time}")
            
            return f"Upcoming events:\n" + "\n".join(event_list)
        except Exception as e:
            return f"Error getting calendar events: {str(e)}"
    
    def _create_calendar_event(self, event_details: str) -> str:
        """
        Create a new calendar event
        """
        try:
            # Parse event details from the input
            # This is a simplified parser - in production you'd want more robust parsing
            lines = event_details.split('\n')
            title = ""
            start_time = ""
            end_time = ""
            description = ""
            
            for line in lines:
                if line.startswith("Title:"):
                    title = line.replace("Title:", "").strip()
                elif line.startswith("Start:"):
                    start_time = line.replace("Start:", "").strip()
                elif line.startswith("End:"):
                    end_time = line.replace("End:", "").strip()
                elif line.startswith("Description:"):
                    description = line.replace("Description:", "").strip()
            
            if not all([title, start_time, end_time]):
                return "Please provide title, start time, and end time for the event."
            
            event = self.calendar_manager.create_event(
                summary=title,
                start_time=start_time,
                end_time=end_time,
                description=description
            )
            
            return f"Event '{title}' created successfully with ID: {event['id']}"
        except Exception as e:
            return f"Error creating calendar event: {str(e)}"
    
    def _delete_calendar_event(self, event_id: str) -> str:
        """
        Delete a calendar event
        """
        try:
            success = self.calendar_manager.delete_event(event_id)
            if success:
                return f"Event with ID {event_id} deleted successfully."
            else:
                return f"Failed to delete event with ID {event_id}."
        except Exception as e:
            return f"Error deleting calendar event: {str(e)}"
    
    def _update_calendar_event(self, update_details: str) -> str:
        """
        Update an existing calendar event
        """
        try:
            # Parse update details
            lines = update_details.split('\n')
            event_id = ""
            updates = {}
            
            for line in lines:
                if line.startswith("Event ID:"):
                    event_id = line.replace("Event ID:", "").strip()
                elif line.startswith("Summary:"):
                    updates['summary'] = line.replace("Summary:", "").strip()
                elif line.startswith("Description:"):
                    updates['description'] = line.replace("Description:", "").strip()
                elif line.startswith("Location:"):
                    updates['location'] = line.replace("Location:", "").strip()
                elif line.startswith("Start Time:"):
                    updates['start_time'] = line.replace("Start Time:", "").strip()
                elif line.startswith("End Time:"):
                    updates['end_time'] = line.replace("End Time:", "").strip()
            
            if not event_id:
                return "Please provide the Event ID to update."
            
            updated_event = self.calendar_manager.update_event(event_id, **updates)
            return f"Event '{updated_event['summary']}' updated successfully."
        except Exception as e:
            return f"Error updating calendar event: {str(e)}"
    
    async def get_calendar_events(self) -> List[Dict[str, Any]]:
        """
        Get calendar events for API endpoint
        """
        return self.calendar_manager.get_upcoming_events() 