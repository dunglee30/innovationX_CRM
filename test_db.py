# db_setup.py
import boto3
from botocore.exceptions import ClientError
import os
import random
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv() # Load env vars here too for setup script
DYNAMODB_ENDPOINT_URL = os.getenv('DYNAMODB_ENDPOINT_URL', 'http://localhost:8000')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'AKIAIOSFODNN7EXAMPLE')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY')
# ...

USERS_TABLE_NAME = os.getenv('USERS_TABLE_NAME', 'Users')
EVENTS_TABLE_NAME = os.getenv('EVENTS_TABLE_NAME', 'Events')
USER_EVENT_RELATIONS_TABLE_NAME = os.getenv('USER_EVENT_RELATIONS_TABLE_NAME', 'UserEventRelations')

# --- Boto3 Clients and Resources ---
dynamodb_client = boto3.client(
    'dynamodb',
    region_name=AWS_REGION,
    endpoint_url=DYNAMODB_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
dynamodb_resource = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    endpoint_url=DYNAMODB_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def query_relations_by_role_and_min_events(
    role: str, min_events: int
):
    """
    Scans the UserEventRelations table for users with a specific role
    who have hosted at least a minimum number of events.
    Uses scan with ExpressionAttributeNames for reserved keyword compatibility.
    """
    try:
        table = dynamodb_resource.Table(USER_EVENT_RELATIONS_TABLE_NAME)
        response = table.scan(
            FilterExpression="#role = :role",
            ExpressionAttributeNames={
                "#role": "role"
            },
            ExpressionAttributeValues={
                ":role": role
            }
        )
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error querying UserEventRelations: {e}")
        return []

if __name__ == "__main__":
    # Example usage
    role = "host"
    min_events = 5
    relations = query_relations_by_role_and_min_events(role, min_events)
    if relations:
        print(f"Found {len(relations)} users with role '{role}' who have hosted at least {min_events} events.")
    else:
        print(f"No users found with role '{role}' who have hosted at least {min_events} events.")