# app/models/event.py

from pydantic import BaseModel, Field
from typing import Optional, List 

class Event(BaseModel):
    event_id: str = Field(..., example="e1", description="Unique identifier for the event.")
    slug: str = Field(..., example="fastapi-basics-workshop", description="URL-friendly identifier for the event.")
    title: str = Field(..., example="FastAPI Basics Workshop", description="Title of the event.")
    description: Optional[str] = Field(None, example="An introductory workshop on FastAPI.", description="Detailed description of the event.")
    start_at: str = Field(..., example="2025-08-01T10:00:00Z", description="Start date and time of the event (ISO 8601 format).")
    end_at: str = Field(..., example="2025-08-01T12:00:00Z", description="End date and time of the event (ISO 8601 format).")
    venue: str = Field(..., example="Online via Zoom", description="Location or platform where the event takes place.")
    max_capacity: Optional[int] = Field(None, example=100, description="Maximum number of attendees for the event.")

    # class Config:
    #     populate_by_name = True
class EventRequest(BaseModel):
    slug: str = Field(..., example="fastapi-basics-workshop", description="URL-friendly identifier for the event.")
    title: str = Field(..., example="FastAPI Basics Workshop", description="Title of the event.")
    description: Optional[str] = Field(None, example="An introductory workshop on FastAPI.", description="Detailed description of the event.")
    start_at: str = Field(..., example="2025-08-01T10:00:00Z", description="Start date and time of the event (ISO 8601 format).")
    end_at: str = Field(..., example="2025-08-01T12:00:00Z", description="End date and time of the event (ISO 8601 format).")
    venue: str = Field(..., example="Online via Zoom", description="Location or platform where the event takes place.")
    max_capacity: Optional[int] = Field(None, example=100, description="Maximum number of attendees for the event.")