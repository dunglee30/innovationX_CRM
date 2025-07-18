# app/models/event.py
# Suitable for Python 3.9+
from pydantic import BaseModel, Field
from typing import Optional, List # Use typing.Optional and typing.List for Python 3.9 compatibility

class Event(BaseModel):
    event_id: str = Field(..., alias="id", example="e1", description="Unique identifier for the event.")
    slug: str = Field(..., example="fastapi-basics-workshop", description="URL-friendly identifier for the event.")
    title: str = Field(..., example="FastAPI Basics Workshop", description="Title of the event.")
    description: Optional[str] = Field(None, example="An introductory workshop on FastAPI.", description="Detailed description of the event.")
    start_at: str = Field(..., alias="startAt", example="2025-08-01T10:00:00Z", description="Start date and time of the event (ISO 8601 format).")
    end_at: str = Field(..., alias="endAt", example="2025-08-01T12:00:00Z", description="End date and time of the event (ISO 8601 format).")
    venue: str = Field(..., example="Online via Zoom", description="Location or platform where the event takes place.")
    max_capacity: Optional[int] = Field(None, alias="maxCapacity", example=100, description="Maximum number of attendees for the event.")
    owner_id: str = Field(..., alias="owner", example="u1", description="ID of the user who owns/created the event.")
    host_ids: List[str] = Field(..., alias="hosts", example=["u1", "u2"], description="List of user IDs who are hosts for the event.")

    class Config:
        populate_by_name = True