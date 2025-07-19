# app/repositories/event_repository.py
from app.repositories.base_repository import BaseRepository
from app.core.config import EMAIL_LOGS_TABLE_NAME
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

class EmailLogsRepository(BaseRepository):
    def __init__(self):
        super().__init__(EMAIL_LOGS_TABLE_NAME) # Uses the table name defined in config

    def log_email_status(self, email_id: str, recipient_email: str, status: str):
        """Store the status of a sent email in the EmailLogs table."""
        try:
            self.table.put_item(Item={
                "email_id": email_id,
                "recipient_email": recipient_email,
                "status": status
            })
        except ClientError as e:
            logger.error(f"Failed to log email status for {recipient_email}: {e}")
            raise
    
    def get_email_logs(self, limit: int = 10, exclusive_start_key: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Retrieve email logs with pagination."""
        scan_kwargs = {"Limit": limit}
        if exclusive_start_key:
            scan_kwargs["ExclusiveStartKey"] = exclusive_start_key
        
        try:
            response = self.table.scan(**scan_kwargs)
            logger.debug(f"Raw DynamoDB scan response: {response}")
            return {
                "items": response.get('Items', []),
                "last_evaluated_key": response.get('LastEvaluatedKey')
            }
        except ClientError as e:
            logger.error(f"Failed to retrieve email logs: {e}")
            raise

