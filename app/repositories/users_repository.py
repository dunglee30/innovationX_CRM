# app/repositories/user_repository.py
from app.repositories.base_repository import BaseRepository
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError

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