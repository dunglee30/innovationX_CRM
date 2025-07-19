# app/models/relation.py

from pydantic import BaseModel, Field
from typing import Optional, List 
class UserEventRelation(BaseModel):
    PK: str
    SK: str
    GSI1_PK: str
    GSI1_SK: str
    type: str # e.g., "EventOwnership", "EventHosting"
    user_id: str
    role: str # e.g., "owner", "host", "attendee"
    first_name: Optional[str] = None 
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    event_id: str
    event_title: Optional[str] = Field(None) 
    event_date: Optional[str] = None
    user_event_id: str  # Unique ID for the user-event relation, if needed

    # class Config:
    #     populate_by_name = True


class UserEventListItem(BaseModel):
    event_id: str = Field(..., example="e1")
    event_title: str = Field(..., example="FastAPI Basics Workshop") 
    role: str = Field(..., example="owner")
    event_date: Optional[str] = None

    # class Config:
    #     populate_by_name = True

class EventUserListItem(BaseModel):
    user_id: str = Field(..., example="u1")
    first_name: Optional[str] = Field(None) 
    last_name: Optional[str] = Field(None)   
    role: str = Field(..., example="owner")
    phone_number: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    job_title: Optional[str] = Field(None)
    company: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    state: Optional[str] = Field(None)

    # class Config:
    #     populate_by_name = True