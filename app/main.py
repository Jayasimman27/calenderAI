from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from .models import ChatMessage, ChatResponse
from .agent import TailorTalkAgent

app = FastAPI(title="TailorTalk API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent
agent = TailorTalkAgent()

@app.get("/")
async def root():
    return {"message": "Welcome to TailorTalk API"}

@app.get("/health")
async def health_check():
    try:
        # Test basic functionality
        return {
            "status": "healthy", 
            "timestamp": datetime.utcnow().isoformat(),
            "message": "TailorTalk API is running"
        }
    except Exception as e:
        return {
            "status": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Process a chat message and return the agent's response
    """
    try:
        response = await agent.process_message(message.content)
        return ChatResponse(
            message=response,
            timestamp=message.timestamp or datetime.utcnow(),
            success=True,
            error=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/calendar/events")
async def get_calendar_events():
    """
    Get upcoming calendar events
    """
    try:
        events = agent.calendar_manager.get_upcoming_events()
        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calendar/events")
async def create_calendar_event(event_data: dict):
    """
    Create a new calendar event
    """
    try:
        # Use the calendar manager directly
        event = agent.calendar_manager.create_event(
            summary=event_data["summary"],
            start_time=event_data["start_time"],
            end_time=event_data["end_time"],
            description=event_data.get("description", ""),
            location=event_data.get("location", "")
        )
        return {"event": event, "message": "Event created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/calendar/events/{event_id}")
async def delete_calendar_event(event_id: str):
    """
    Delete a calendar event
    """
    try:
        success = agent.calendar_manager.delete_event(event_id)
        if success:
            return {"message": "Event deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Event not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8004))
    uvicorn.run(app, host="0.0.0.0", port=port) 