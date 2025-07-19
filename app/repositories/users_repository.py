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
    
    def get_users_by_filter(self, filter_list: list, limit: int = 10, exclusive_start_key: dict = None, sort_by: str = None, sort_order: str = "asc") -> dict:
        """Generic filter, pagination, and sorting for Users table. Returns up to `limit` items after filtering."""
        scan_batch_size = 10
        scan_kwargs = {"Limit": scan_batch_size}
        # Build filter expression
        if filter_list:
            filter_expr = None
            for f in filter_list:
                key = f.field
                value = f.value
                if key and value is not None:
                    expr = Attr(key).contains(value)
                    filter_expr = expr if filter_expr is None else filter_expr & expr
            if filter_expr is not None:
                scan_kwargs["FilterExpression"] = filter_expr
        if exclusive_start_key:
            scan_kwargs["ExclusiveStartKey"] = exclusive_start_key
        items = []
        last_evaluated_key = None
        try:
            while len(items) < limit:
                response = self.table.scan(**scan_kwargs)
                logger.debug(f"Raw DynamoDB scan response: {response}")
                batch = response.get('Items', [])
                items.extend(batch)
                last_evaluated_key = response.get('LastEvaluatedKey')
                if not last_evaluated_key:
                    break
                scan_kwargs["ExclusiveStartKey"] = last_evaluated_key
            # Only return up to `limit` items
            # --- Sorting logic ---
            if sort_by:
                items = sorted(
                    items,
                    key=lambda x: x.get(sort_by, ""),
                    reverse=(sort_order == "desc")
                )
            return {
                "items": items[:limit],
                "last_evaluated_key": last_evaluated_key if len(items) >= limit else None
            }
        except ClientError as e:
            print(f"DynamoDB ClientError in UserRepository.get_users_by_filter: {e}")
            raise

    def create_user(self, user_data: dict) -> None:
        """Creates a new user in the Users table."""
        try:
            self.table.put_item(Item=user_data)
        except ClientError as e:
            print(f"DynamoDB ClientError in UserRepository.create_user: {e}")
            raise

    def update_user(self, user_id: str, user_data: dict) -> dict:
        """Updates an existing user in the Users table, handling reserved keywords."""
        try:
            update_expr_parts = []
            expr_attr_values = {}
            expr_attr_names = {}
            for k, v in user_data.items():
                if k != "user_id":
                    placeholder = f":{k}"
                    name_placeholder = f"#{k}" if k in ["state"] else k
                    update_expr_parts.append(f"{name_placeholder} = {placeholder}")
                    expr_attr_values[placeholder] = v
                    if k in ["state"]:
                        expr_attr_names[name_placeholder] = k
            update_expr = "SET " + ", ".join(update_expr_parts)
            response = self.table.update_item(
                Key={"user_id": user_id},
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_attr_values,
                ExpressionAttributeNames=expr_attr_names if expr_attr_names else None,
                ReturnValues="ALL_NEW"
            )
            return response.get("Attributes")
        except ClientError as e:
            print(f"DynamoDB ClientError in UserRepository.update_user: {e}")
            raise

    def delete_user(self, user_id: str) -> None:
        """Deletes a user from the Users table."""
        try:
            self.table.delete_item(Key={"user_id": user_id})
        except ClientError as e:
            print(f"DynamoDB ClientError in UserRepository.delete_user: {e}")
            raise