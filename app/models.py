from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    """
    Model for incoming chat messages
    """
    content: str = Field(..., description="The message content")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Message timestamp")
    user_id: Optional[str] = Field(None, description="User identifier")
    access_token: Optional[str] = Field(None, description="Google OAuth access token for calendar actions")

class ChatResponse(BaseModel):
    """
    Model for chat responses
    """
    message: str = Field(..., description="The response message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    success: bool = Field(True, description="Whether the operation was successful")
    error: Optional[str] = Field(None, description="Error message if any")

class CalendarEvent(BaseModel):
    """
    Model for calendar events
    """
    id: str = Field(..., description="Event ID")
    summary: str = Field(..., description="Event title/summary")
    start: str = Field(..., description="Start time in ISO format")
    end: str = Field(..., description="End time in ISO format")
    description: Optional[str] = Field(None, description="Event description")
    location: Optional[str] = Field(None, description="Event location")

class CreateEventRequest(BaseModel):
    """
    Model for creating calendar events
    """
    summary: str = Field(..., description="Event title")
    start_time: str = Field(..., description="Start time in ISO format")
    end_time: str = Field(..., description="End time in ISO format")
    description: Optional[str] = Field(None, description="Event description")
    location: Optional[str] = Field(None, description="Event location")

class UpdateEventRequest(BaseModel):
    """
    Model for updating calendar events
    """
    event_id: str = Field(..., description="Event ID to update")
    summary: Optional[str] = Field(None, description="New event title")
    start_time: Optional[str] = Field(None, description="New start time in ISO format")
    end_time: Optional[str] = Field(None, description="New end time in ISO format")
    description: Optional[str] = Field(None, description="New event description")
    location: Optional[str] = Field(None, description="New event location")

class CalendarEventsResponse(BaseModel):
    """
    Model for calendar events response
    """
    events: List[CalendarEvent] = Field(..., description="List of calendar events")
    total_count: int = Field(..., description="Total number of events")
    success: bool = Field(True, description="Whether the operation was successful")
    error: Optional[str] = Field(None, description="Error message if any")

class HealthResponse(BaseModel):
    """
    Model for health check response
    """
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")
    version: str = Field("1.0.0", description="API version") 