from pydantic import BaseModel, Field

class EmailLog(BaseModel):
    email_id: str = Field(..., example="email_1", description="Unique identifier for the email log entry.")
    recipient_email: str = Field(..., example="email@example.com", description="Email address of the recipient.")
    status: str = Field(..., example="sent", description="Status of the email (e.g., sent, failed).")