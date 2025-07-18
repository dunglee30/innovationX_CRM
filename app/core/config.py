# app/core/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# --- DynamoDB Configuration ---
DYNAMODB_ENDPOINT_URL = os.getenv('DYNAMODB_ENDPOINT_URL', 'http://localhost:8000')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'AKIAIOSFODNN7EXAMPLE')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY')

# --- Table Names ---
USERS_TABLE_NAME = os.getenv('USERS_TABLE_NAME', 'Users')
EVENTS_TABLE_NAME = os.getenv('EVENTS_TABLE_NAME', 'Events')
USER_EVENT_RELATIONS_TABLE_NAME = os.getenv('USER_EVENT_RELATIONS_TABLE_NAME', 'UserEventRelations')

# Other global settings can go here
API_TITLE = "User and Event Management API"
API_DESCRIPTION = "API to manage users, events, and their relationships using DynamoDB Hybrid Solution."
API_VERSION = "1.0.0"