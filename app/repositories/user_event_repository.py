# app/repositories/user_event_relations_repository.py

from app.repositories.base_repository import BaseRepository
from app.models.users import User
from app.models.user_event import EventUserListItem  # Import EventUserListItem

import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any, List 
import logging
from collections import Counter

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

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
    
    def get_event_users_by_role_and_min_events(self, role: str, min_events: int) -> List[EventUserListItem]:
        """
        Returns EventUserListItem objects for users with the given role who have hosted at least min_events events.
        """
        try:
            logger.debug(f"Fetching relations for role: {role}")
            response = self.table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr('role').eq(role)
            )
            logger.debug(f"Raw DynamoDB scan response for role '{role}': {response}")
            relations = response.get('Items', [])
            user_event_counts = Counter(rel.get('user_id') for rel in relations if 'user_id' in rel)
            filtered_user_ids = [user_id for user_id, count in user_event_counts.items() if count >= min_events]
            # Build EventUserListItem objects from relation data
            users = []
            seen = set()
            for rel in relations:
                user_id = rel.get('user_id')
                if user_id in filtered_user_ids and user_id not in seen:
                    seen.add(user_id)
                    user_data = {k: v for k, v in rel.items() if k in EventUserListItem.__fields__}
                    user_data['user_id'] = user_id  # Ensure user_id is present
                    users.append(EventUserListItem(**rel))
            return users
        except Exception as e:
            logger.error(f"Error in get_event_users_by_role_and_min_events: {e}")
            raise RuntimeError(f"Failed to retrieve users with role '{role}' and hosted event count >= {min_events}: {e}")