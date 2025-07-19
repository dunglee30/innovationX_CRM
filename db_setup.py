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
EMAIL_LOGS_TABLE_NAME = os.getenv('EMAIL_LOGS_TABLE_NAME', 'EmailLogs')
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

# --- Generic Table Creation Function ---
def create_dynamodb_table(table_name, key_schema, attribute_definitions, global_secondary_indexes=None):
    try:
        print(f"Attempting to create table: {table_name}")
        params = {
            'TableName': table_name,
            'KeySchema': key_schema,
            'AttributeDefinitions': attribute_definitions,
            'BillingMode': 'PAY_PER_REQUEST'
        }
        if global_secondary_indexes:
            params['GlobalSecondaryIndexes'] = global_secondary_indexes

        response = dynamodb_client.create_table(**params)
        print(f"Table '{table_name}' creation initiated. Waiting for table to become active...")
        waiter = dynamodb_client.get_waiter('table_exists')
        waiter.wait(TableName=table_name)
        print(f"Table '{table_name}' created successfully and is active.")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table '{table_name}' already exists.")
        else:
            print(f"Error creating table '{table_name}': {e}")
            raise
    except Exception as e:
        print(f"An unexpected error occurred during table creation: {e}")
        raise

# --- Specific Table Creation Function ---
def create_all_tables():
    print("\n--- Creating All DynamoDB Tables ---")
    create_dynamodb_table(USERS_TABLE_NAME, [{'AttributeName': 'user_id', 'KeyType': 'HASH'}], [{'AttributeName': 'user_id', 'AttributeType': 'S'}])
    create_dynamodb_table(EVENTS_TABLE_NAME, [{'AttributeName': 'event_id', 'KeyType': 'HASH'}], [{'AttributeName': 'event_id', 'AttributeType': 'S'}])
    create_dynamodb_table(EMAIL_LOGS_TABLE_NAME, [{'AttributeName': 'email_id', 'KeyType': 'HASH'}], [{'AttributeName': 'email_id', 'AttributeType': 'S'}])
    create_dynamodb_table(
        USER_EVENT_RELATIONS_TABLE_NAME,
        [{'AttributeName': 'PK', 'KeyType': 'HASH'}, {'AttributeName': 'SK', 'KeyType': 'RANGE'}],
        [
            {'AttributeName': 'PK', 'AttributeType': 'S'},
            {'AttributeName': 'SK', 'AttributeType': 'S'},
            {'AttributeName': 'GSI1_PK', 'AttributeType': 'S'},
            {'AttributeName': 'GSI1_SK', 'AttributeType': 'S'},
            {'AttributeName': 'role', 'AttributeType': 'S'},
            {'AttributeName': 'user_event_id', 'AttributeType': 'S'}
        ],
        global_secondary_indexes=[
            {
                'IndexName': 'GSI1_PK-GSI1_SK-index',
                'KeySchema': [
                    {'AttributeName': 'GSI1_PK', 'KeyType': 'HASH'},
                    {'AttributeName': 'GSI1_SK', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
            },
            {
                'IndexName': 'role-user_event-index',
                'KeySchema': [
                    {'AttributeName': 'role', 'KeyType': 'HASH'},
                    {'AttributeName': 'user_event_id', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
            }
        ]
    )

# --- Data Insertion Function ---
def put_sample_data():
    print("\n--- Inserting Sample Data ---")
    users_table = dynamodb_resource.Table(USERS_TABLE_NAME)
    events_table = dynamodb_resource.Table(EVENTS_TABLE_NAME)
    relations_table = dynamodb_resource.Table(USER_EVENT_RELATIONS_TABLE_NAME)

    # --- SAMPLE DATA ---
    new_users_data = [
        {
            'user_id': f'u{n}',
            'first_name': f'User{n}',
            'last_name': f'Last{n}',
            'phone_number': f'+849000000{n:02d}',
            'email': f'user{n}@example.com',
            'avatar': f'https://example.com/avatars/user{n}.jpg',
            'gender': 'Male' if n % 2 == 0 else 'Female',
            'job_title': f'Job Title {random.choice(range(1, 4))}',
            'company': f'Company {random.choice(range(1, 4))}',
            'city': f'City {random.choice(range(1, 6))}',
            'state': f'State {random.choice(range(1, 6))}',
        } for n in range(1, 41)  # Create 40 new users
    ]
    for user in new_users_data:
        users_table.put_item(Item=user)
    print(f"Inserted {len(new_users_data)} new users.")

    new_events_data = [
        {
            'event_id': f'e{n}',
            'slug': f'event-{n}-slug',
            'title': f'Event Title {n}',
            'description': f'Description for event {n}',
            'start_at': f'2025-10-{n:02d}T10:00:00Z',
            'end_at': f'2025-10-{n:02d}T12:00:00Z',
            'venue': f'Venue {n}',
            'max_capacity': 50 + n * 10,
        } for n in range(1, 21)  # Create 20 new events
    ]
    for event in new_events_data:
        events_table.put_item(Item=event)
    print(f"Inserted {len(new_events_data)} new events.")

    roles = ['attendee', 'host']
    relation_types = {'host': 'EventHosting', 'attendee': 'EventAttendance'}
    relations = []
    user_event_pairs = set()  # Track (user_id, event_id) pairs
    attempts = 0
    while len(relations) < 200 and attempts < 5000:
        user = random.choice(new_users_data)
        event = random.choice(new_events_data)
        pair = (user['user_id'], event['event_id'])
        if pair in user_event_pairs:
            attempts += 1
            continue  # Skip if this user already has a role for this event
        role = random.choice(roles)
        relations.append({
            'PK': f"USER#{user['user_id']}",
            'SK': f"EVENT#{event['event_id']}#{role.upper()}",
            'GSI1_PK': f"EVENT#{event['event_id']}",
            'GSI1_SK': f"USER#{user['user_id']}#{role.upper()}",
            'type': relation_types[role],
            'user_id': user['user_id'],
            'role': role,
            'user_event_id': f"{user['user_id']}#{event['event_id']}",
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'phone_number': user['phone_number'],
            'email': user['email'],
            'job_title': user['job_title'],
            'company': user['company'],
            'city': user['city'],
            'state': user['state'],
            'event_id': event['event_id'],
            'event_title': event['title'],
            'event_date': event['start_at']
        })
        user_event_pairs.add(pair)
        attempts += 1
    for rel in relations:
        relations_table.put_item(Item=rel)
    print(f"Inserted {len(relations)} new relations.")

def delete_table_if_exists(table_name):
    try:
        existing_tables = dynamodb_client.list_tables()['TableNames']
        if table_name in existing_tables:
            print(f"Deleting table: {table_name}")
            dynamodb_client.delete_table(TableName=table_name)
            # Wait for deletion to complete
            waiter = dynamodb_client.get_waiter('table_not_exists')
            waiter.wait(TableName=table_name)
            print(f"Table '{table_name}' deleted.")
    except Exception as e:
        print(f"Error deleting table {table_name}: {e}")

if __name__ == '__main__':
    # Drop all tables before creating new ones
    delete_table_if_exists(USERS_TABLE_NAME)
    delete_table_if_exists(EVENTS_TABLE_NAME)
    delete_table_if_exists(USER_EVENT_RELATIONS_TABLE_NAME)
    create_all_tables()
    put_sample_data()
    print("\nDynamoDB table setup and data insertion complete.")