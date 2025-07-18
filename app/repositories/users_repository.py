# app/repositories/user_repository.py
from app.repositories.base_repository import BaseRepository
from typing import Dict, Any, Optional, List
from botocore.exceptions import ClientError
import boto3

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
    
    def get_user_by_company(self, company: str) -> List[Dict[str, Any]]:
        """Retrieves all users whose company name contains the given string."""
        try:
            response = self.table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr('company').contains(company)
            )
            return response.get('Items', [])
        except ClientError as e:
            print(f"DynamoDB ClientError in UserRepository.get_user_by_company for {company}: {e}")
            raise
    
    def get_user_by_job_title(self, job_title: str) -> Optional[Dict[str, Any]]:
        """Retrieves a user's profile by job title."""
        try:
            response = self.table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr('job_title').contains(job_title)
            )
            items = response.get('Items', [])
            return items[0] if items else None
        except ClientError as e:
            print(f"DynamoDB ClientError in UserRepository.get_user_by_job_title for {job_title}: {e}")
            raise
    
    def get_user_by_City_and_State(self, city: str, state: str) -> Optional[Dict[str, Any]]:
        """Retrieves a user's profile by city and state."""
        try:
            response = self.table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr('city').contains(city) &
                                 boto3.dynamodb.conditions.Attr('state').contains(state)
            )
            items = response.get('Items', [])
            return items[0] if items else None
        except ClientError as e:
            print(f"DynamoDB ClientError in UserRepository.get_user_by_City_and_State for {city}, {state}: {e}")
            raise
    

    def get_all_users(self) -> List[Dict[str, Any]]:
        """Retrieves all users from the Users table."""
        try:
            response = self.table.scan()
            return response.get('Items', [])
        except ClientError as e:
            print(f"DynamoDB ClientError in UserRepository.get_all_users: {e}")
            raise