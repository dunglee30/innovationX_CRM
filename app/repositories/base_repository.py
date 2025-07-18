# app/repositories/base_repository.py
from app.core.db_connection import db_connection
from botocore.exceptions import ClientError
from typing import Dict, Any, Optional

class BaseRepository:
    def __init__(self, table_name: str):
        db_connection.initialize() # Ensure DB connection is ready
        self.table = db_connection.dynamodb_resource.Table(table_name)
        try:
            self.table.load() # Verifies table existence and loads metadata
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f"Error: DynamoDB Table '{table_name}' not found. Please ensure it is created.")
            raise # Re-raise for higher-level handling
        except Exception as e:
            print(f"Error initializing repository for table '{table_name}': {e}")
            raise