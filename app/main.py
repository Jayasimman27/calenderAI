from dotenv import load_dotenv

load_dotenv()

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, SecretStr
from typing import List, Optional
from datetime import datetime
import uvicorn
import sys

# Load environment variables

print('DEBUG: Current working directory:', os.getcwd())
print('DEBUG: MISTRAL_API_KEY from env:', os.environ.get('MISTRAL_API_KEY'))
api_key = os.environ.get('MISTRAL_API_KEY')
if not api_key:
    print('ERROR: MISTRAL_API_KEY environment variable not set. Please check your .env file and restart the backend.')
    sys.exit(1)

from .models import ChatMessage, ChatResponse
from langchain.agents import initialize_agent, AgentType
from langchain_mistralai.chat_models import ChatMistralAI
from app.langchain_tools import tools

app = FastAPI(title="TailorTalk API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LangChain agent
llm = ChatMistralAI(api_key=SecretStr(api_key))
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to TailorTalk API",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }

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
    Process a chat message and return the agent's response using LangChain
    """
    try:
        print("DEBUG: ChatMessage received:", message)
        print("DEBUG: access_token:", message.access_token)
        # Pass only the user message string as a dict with 'input' key
        response = agent.invoke({"input": message.content})
        # Ensure response is a string for ChatResponse
        if isinstance(response, dict):
            response_message = response.get('output', str(response))
        else:
            response_message = str(response)
        return ChatResponse(
            message=response_message,
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
        # The calendar manager is no longer part of TailorTalkAgent,
        # so this endpoint will need to be refactored or removed if not used.
        # For now, returning a placeholder message.
        return {"message": "Calendar functionality is currently disabled."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calendar/events")
async def create_calendar_event(event_data: dict):
    """
    Create a new calendar event
    """
    try:
        # Use the calendar manager directly
        # The calendar manager is no longer part of TailorTalkAgent,
        # so this endpoint will need to be refactored or removed if not used.
        # For now, returning a placeholder message.
        return {"message": "Calendar functionality is currently disabled."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/calendar/events/{event_id}")
async def delete_calendar_event(event_id: str):
    """
    Delete a calendar event
    """
    try:
        # The calendar manager is no longer part of TailorTalkAgent,
        # so this endpoint will need to be refactored or removed if not used.
        # For now, returning a placeholder message.
        return {"message": "Calendar functionality is currently disabled."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/calendar/events/{event_id}")
async def update_calendar_event(event_id: str, event_data: dict):
    """
    Update an existing calendar event
    """
    try:
        # The calendar manager is no longer part of TailorTalkAgent,
        # so this endpoint will need to be refactored or removed if not used.
        # For now, returning a placeholder message.
        return {"message": "Calendar functionality is currently disabled."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/calendar/events/search")
async def search_calendar_events(query: str):
    """
    Search for calendar events by title
    """
    try:
        # The calendar manager is no longer part of TailorTalkAgent,
        # so this endpoint will need to be refactored or removed if not used.
        # For now, returning a placeholder message.
        return {"message": "Calendar functionality is currently disabled."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/calendar/events/{event_id}")
async def get_calendar_event(event_id: str):
    """
    Get a specific calendar event by ID
    """
    try:
        # The calendar manager is no longer part of TailorTalkAgent,
        # so this endpoint will need to be refactored or removed if not used.
        # For now, returning a placeholder message.
        return {"message": "Calendar functionality is currently disabled."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8004))
    uvicorn.run(app, host="0.0.0.0", port=port) 