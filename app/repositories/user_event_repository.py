# app/repositories/user_event_relations_repository.py

from app.repositories.base_repository import BaseRepository
import boto3
from typing import Dict, Any, List 

class UserEventRelationsRepository(BaseRepository):
    def __init__(self):
        super().__init__("UserEventRelations") # Uses the table name defined in config
        self.gsi_index_name = 'GSI1_PK-GSI1_SK-index'

    def get_events_for_user(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all events (owned/hosted/etc.) for a given user
        using the main table's PK.
        """
        try:
            response = self.table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('PK').eq(f'USER#{user_id}') &
                                     boto3.dynamodb.conditions.Key('SK').begins_with('EVENT#')
            )
            return response.get('Items', [])
        except ClientError as e:
            print(f"DynamoDB ClientError in UserEventRelationsRepository.get_events_for_user for {user_id}: {e}")
            raise

    def get_users_for_event(self, event_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all users (owner/hosts/etc.) for a given event
        using the GSI.
        """
        try:
            response = self.table.query(
                IndexName=self.gsi_index_name,
                KeyConditionExpression=boto3.dynamodb.conditions.Key('GSI1_PK').eq(f'EVENT#{event_id}') &
                                     boto3.dynamodb.conditions.Key('GSI1_SK').begins_with('USER#')
            )
            return response.get('Items', [])
        except ClientError as e:
            print(f"DynamoDB ClientError in UserEventRelationsRepository.get_users_for_event for {event_id}: {e}")
            raise