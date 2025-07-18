# app/repositories/user_repository.py
from app.repositories.base_repository import BaseRepository
from typing import Dict, Any, Optional, List
from botocore.exceptions import ClientError
import boto3
from boto3.dynamodb.conditions import Attr
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__("Users") # Uses the table name defined in config

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a user's profile by ID."""
        try:
            response = self.table.get_item(Key={'user_id': user_id})
            return response.get('Item')
        except ClientError as e:
            # Log the error, but re-raise for consistent error handling in router
            print(f"DynamoDB ClientError in UserRepository.get_user_by_id for {user_id}: {e}")
            raise
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Retrieves all users from the Users table."""
        try:
            response = self.table.scan()
            return response.get('Items', [])
        except ClientError as e:
            print(f"DynamoDB ClientError in UserRepository.get_all_users: {e}")
            raise
    
    def get_users_by_filter(self, filter_list: list, limit: int = 10, exclusive_start_key: dict = None) -> dict:
        """Generic filter and pagination for Users table."""
        scan_kwargs = {"Limit": limit}
        # Build filter expression
        if filter_list:
            filter_expr = None
            for f in filter_list:
                key = f.get("key")
                value = f.get("value")
                if key and value is not None:
                    expr = Attr(key).contains(value)
                    filter_expr = expr if filter_expr is None else filter_expr & expr
            if filter_expr is not None:
                scan_kwargs["FilterExpression"] = filter_expr
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
            print(f"DynamoDB ClientError in UserRepository.get_users_by_filter: {e}")
            raise