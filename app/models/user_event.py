# app/models/relation.py
# Suitable for Python 3.9+
from pydantic import BaseModel, Field
from typing import Optional, List # Use typing.Optional and typing.List for Python 3.9 compatibility

# This model represents an item as it might be stored in the UserEventRelations table
class UserEventRelation(BaseModel):
    PK: str
    SK: str
    GSI1_PK: str
    GSI1_SK: str
    type: str # e.g., "EventOwnership", "EventHosting"
    user_id: str
    event_id: str
    role: str # e.g., "owner", "host", "attendee"
    username: Optional[str] = None # Denormalized for display
    first_name: Optional[str] = None # Denormalized new field
    last_name: Optional[str] = None  # Denormalized new field
    event_title: Optional[str] = Field(None, alias="title") # Denormalized new field (from 'title')
    event_date: Optional[str] = None # Denormalized for display

    class Config:
        populate_by_name = True


# These models are for outputting lists of related items from the relations table queries
class UserEventListItem(BaseModel):
    event_id: str = Field(..., example="e1")
    title: str = Field(..., example="FastAPI Basics Workshop", alias="event_title") # Alias to match 'title'
    role: str = Field(..., example="owner")
    event_date: Optional[str] = None

    class Config:
        populate_by_name = True

class EventUserListItem(BaseModel):
    user_id: str = Field(..., example="u1")
    username: str = Field(..., example="Alice")
    first_name: Optional[str] = Field(None, alias="firstName") # Alias to match 'firstName'
    last_name: Optional[str] = Field(None, alias="lastName")   # Alias to match 'lastName'
    role: str = Field(..., example="owner")

    class Config:
        populate_by_name = True