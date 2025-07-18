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
    event_id: str
    role: str # e.g., "owner", "host", "attendee"
    first_name: Optional[str] = None 
    last_name: Optional[str] = None  
    event_title: Optional[str] = Field(None) 
    event_date: Optional[str] = None 

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

    # class Config:
    #     populate_by_name = True