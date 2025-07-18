# app/core/db_connection.py
import boto3
from botocore.exceptions import ClientError
from app.core.config import DYNAMODB_ENDPOINT_URL, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

class DynamoDBConnection:
    _instance = None
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DynamoDBConnection, cls).__new__(cls)
        return cls._instance

    def initialize(self):
        if not self._is_initialized:
            try:
                # Use boto3.resource for higher-level operations (put_item, get_item, query)
                self.dynamodb_resource = boto3.resource(
                    'dynamodb',
                    region_name=AWS_REGION,
                    endpoint_url=DYNAMODB_ENDPOINT_URL,
                    aws_access_key_id=AWS_ACCESS_KEY_ID,          
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY 
                )
                self._is_initialized = True
                print("DynamoDB connection initialized.")
            except Exception as e:
                print(f"Failed to initialize DynamoDB connection: {e}")
                raise

# Instantiate the connection once. This will be imported by repositories.
db_connection = DynamoDBConnection()