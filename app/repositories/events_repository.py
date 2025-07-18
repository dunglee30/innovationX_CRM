# app/repositories/event_repository.py
from app.repositories.base_repository import BaseRepository
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError

class EventRepository(BaseRepository):
    def __init__(self):
        super().__init__("Events") # Uses the table name defined in config

    def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves an event's details by ID."""
        try:
            response = self.table.get_item(Key={'event_id': event_id})
            return response.get('Item')
        except ClientError as e:
            print(f"DynamoDB ClientError in EventRepository.get_event_by_id for {event_id}: {e}")
            raise