# app/models/user.py

from pydantic import BaseModel, Field
from typing import Optional 

class User(BaseModel):
    user_id: str = Field(..., example="u1", description="Unique identifier for the user.")
    first_name: str = Field(..., example="Alice", description="User's first name.")
    last_name: str = Field(..., example="Smith", description="User's last name.")
    phone_number: str = Field(..., example="+84123456789", description="User's phone number.")
    email: str = Field(..., example="alice@example.com", description="User's email address (unique).")
    avatar: Optional[str] = Field(None, example="http://example.com/avatars/u1.jpg", description="URL to the user's avatar image.")
    gender: Optional[str] = Field(None, example="Female", description="User's gender.")
    job_title: Optional[str] = Field(None, example="Senior Developer", description="User's job title.")
    company: Optional[str] = Field(None, example="Tech Solutions Inc.", description="User's company.")
    city: Optional[str] = Field(None, example="Ho Chi Minh City", description="User's current city.")
    state: Optional[str] = Field(None, example="Ho Chi Minh", description="User's current state/province.")

    # class Config:
    #     populate_by_name = True # Might be used to work with alias later
class UserRequest(BaseModel):
    first_name: str = Field(..., example="Alice", description="User's first name.")
    last_name: str = Field(..., example="Smith", description="User's last name.")
    phone_number: str = Field(..., example="+84123456789", description="User's phone number.")
    email: str = Field(..., example="alice@example.com", description="User's email address (unique).")
    avatar: Optional[str] = Field(None, example="http://example.com/avatars/u1.jpg", description="URL to the user's avatar image.")
    gender: Optional[str] = Field(None, example="Female", description="User's gender.")
    job_title: Optional[str] = Field(None, example="Senior Developer", description="User's job title.")
    company: Optional[str] = Field(None, example="Tech Solutions Inc.", description="User's company.")
    city: Optional[str] = Field(None, example="Ho Chi Minh City", description="User's current city.")
    state: Optional[str] = Field(None, example="Ho Chi Minh", description="User's current state/province.")
