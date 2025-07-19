# app/repositories/event_repository.py
from app.repositories.base_repository import BaseRepository
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

class EventRepository(BaseRepository):
    def __init__(self):
        super().__init__("Events") # Uses the table name defined in config

    def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves an event's details by ID. Returns None if not found."""
        try:
            response = self.table.get_item(Key={'event_id': event_id})
            logger.debug(f"Retrieved event data for ID {event_id}: {response}")
            # item = response.get('Item')
            if 'Item' not in response:
                return None
            return response.get('Item')
        except ClientError as e:
            print(f"DynamoDB ClientError in EventRepository.get_event_by_id for {event_id}: {e}")
            raise

    def create_event(self, event_data: dict) -> None:
        """Creates a new event in the Events table."""
        try:
            self.table.put_item(Item=event_data)
        except ClientError as e:
            print(f"DynamoDB ClientError in EventRepository.create_event: {e}")
            raise

    def update_event(self, event_id: str, event_data: dict) -> dict:
        """Updates an existing event in the Events table."""
        try:
            update_expr_parts = []
            expr_attr_values = {}
            for k, v in event_data.items():
                if k != "event_id":
                    placeholder = f":{k}"
                    update_expr_parts.append(f"{k} = {placeholder}")
                    expr_attr_values[placeholder] = v
            update_expr = "SET " + ", ".join(update_expr_parts)
            logger.debug(f"Updating event with ID: {event_id} with query {update_expr}")
            response = self.table.update_item(
                Key={"event_id": event_id},
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_attr_values,
                ReturnValues="ALL_NEW"
            )
            logger.debug(f"Event updated successfully: {response}")
            return response.get("Attributes")
        except ClientError as e:
            print(f"DynamoDB ClientError in EventRepository.update_event: {e}")
            raise

    def delete_event(self, event_id: str) -> None:
        """Deletes an event from the Events table."""
        try:
            self.table.delete_item(Key={"event_id": event_id})
        except ClientError as e:
            print(f"DynamoDB ClientError in EventRepository.delete_event: {e}")
            raise