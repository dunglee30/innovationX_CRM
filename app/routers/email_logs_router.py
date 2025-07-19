from fastapi import APIRouter, Depends, HTTPException, Query

from typing import List

from app.models.emails_log import EmailLog

from app.repositories.email_logs_repository import EmailLogsRepository 

from app.dependencies import get_email_logs_repo

router = APIRouter(
    prefix="/email_logs",
    tags=["Email Logs"]
)   
@router.get(
    "/",
    summary="Get Email Logs",
    response_model=List[EmailLog],
    description="Retrieves email logs from the EmailLogs table."
)  
async def get_email_logs(
    limit: int = Query(10, ge=1, le=100, description="Maximum number of email logs to retrieve"),
    exclusive_start_key: str = Query(None, description="Exclusive start key for pagination")
):
    """
    Retrieves email logs with pagination.
    """
    email_logs_repo = get_email_logs_repo()
    
    try:
        exclusive_start_key_obj = None
        if exclusive_start_key:
            exclusive_start_key_obj = {"email_id": exclusive_start_key}
        response = email_logs_repo.get_email_logs(limit=limit, exclusive_start_key=exclusive_start_key_obj)
        return [EmailLog(**item) for item in response.get('items', [])]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")