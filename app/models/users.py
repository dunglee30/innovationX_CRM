# app/models/user.py
# Suitable for Python 3.9+
from pydantic import BaseModel, Field
from typing import Optional # Use typing.Optional for Python 3.9 compatibility

class User(BaseModel):
    user_id: str = Field(..., alias="id", example="u1", description="Unique identifier for the user.")
    first_name: str = Field(..., alias="firstName", example="Alice", description="User's first name.")
    last_name: str = Field(..., alias="lastName", example="Smith", description="User's last name.")
    phone_number: str = Field(..., alias="phoneNumber", example="+84123456789", description="User's phone number.")
    email: str = Field(..., example="alice@example.com", description="User's email address (unique).")
    avatar: Optional[str] = Field(None, example="http://example.com/avatars/u1.jpg", description="URL to the user's avatar image.")
    gender: Optional[str] = Field(None, example="Female", description="User's gender.")
    job_title: Optional[str] = Field(None, alias="jobTitle", example="Senior Developer", description="User's job title.")
    company: Optional[str] = Field(None, example="Tech Solutions Inc.", description="User's company.")
    city: Optional[str] = Field(None, example="Ho Chi Minh City", description="User's current city.")
    state: Optional[str] = Field(None, example="Ho Chi Minh", description="User's current state/province.")

    class Config:
        populate_by_name = True # Allow initialization by field name or alias
        # This is for converting Pydantic models to/from dicts (e.g., for DynamoDB)
        # It's especially useful when dealing with aliases.
        # This allows you to interact with the model using `first_name` but have it map to `firstName` in JSON/dict.
        # For DynamoDB, it's generally best to store in the snake_case format or match the alias precisely.
        # For simplicity, we'll store snake_case in DynamoDB, and aliases handle API input/output.