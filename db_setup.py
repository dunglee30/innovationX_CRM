# db_setup.py
import boto3
from botocore.exceptions import ClientError
import os
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
    create_dynamodb_table(
        USER_EVENT_RELATIONS_TABLE_NAME,
        [{'AttributeName': 'PK', 'KeyType': 'HASH'}, {'AttributeName': 'SK', 'KeyType': 'RANGE'}],
        [
            {'AttributeName': 'PK', 'AttributeType': 'S'},
            {'AttributeName': 'SK', 'AttributeType': 'S'},
            {'AttributeName': 'GSI1_PK', 'AttributeType': 'S'},
            {'AttributeName': 'GSI1_SK', 'AttributeType': 'S'}
        ],
        global_secondary_indexes=[{
            'IndexName': 'GSI1_PK-GSI1_SK-index',
            'KeySchema': [{'AttributeName': 'GSI1_PK', 'KeyType': 'HASH'}, {'AttributeName': 'GSI1_SK', 'KeyType': 'RANGE'}],
            'Projection': {'ProjectionType': 'ALL'},
            'ProvisionedThroughput': {'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
        }]
    )

# --- Data Insertion Function ---
def put_sample_data():
    print("\n--- Inserting Sample Data ---")
    users_table = dynamodb_resource.Table(USERS_TABLE_NAME)
    events_table = dynamodb_resource.Table(EVENTS_TABLE_NAME)
    relations_table = dynamodb_resource.Table(USER_EVENT_RELATIONS_TABLE_NAME)

    users_data = [
        {
            'user_id': 'u1',
            'first_name': 'Alice',
            'last_name': 'Smith',
            'phone_number': '+84901234567',
            'email': 'alice@example.com',
            'avatar': 'https://example.com/avatars/alice.jpg',
            'gender': 'Female',
            'job_title': 'Lead Software Engineer',
            'company': 'Innovate Solutions',
            'city': 'Ho Chi Minh City',
            'state': 'Ho Chi Minh'
        },
        {
            'user_id': 'u2',
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'phone_number': '+84912345678',
            'email': 'bob@example.com',
            'avatar': 'https://example.com/avatars/bob.jpg',
            'gender': 'Male',
            'job_title': 'Cloud Architect',
            'company': 'Global Tech Co',
            'city': 'Hanoi',
            'state': 'Hanoi'
        },
        {
            'user_id': 'u3',
            'first_name': 'Charlie',
            'last_name': 'Brown',
            'phone_number': '+84923456789',
            'email': 'charlie@example.com',
            'avatar': 'https://example.com/avatars/charlie.jpg',
            'gender': 'Male',
            'job_title': 'Data Analyst',
            'company': 'Data Insights',
            'city': 'Da Nang',
            'state': 'Da Nang'
        }
    ]
    for user in users_data: users_table.put_item(Item=user)
    print(f"Inserted {len(users_data)} users.")

    events_data = [
        {
            'event_id': 'e1',
            'slug': 'fastapi-basics-workshop',
            'title': 'FastAPI Basics Workshop',
            'description': 'An interactive workshop covering the fundamentals of FastAPI.',
            'start_at': '2025-08-01T10:00:00Z',
            'end_at': '2025-08-01T12:00:00Z',
            'venue': 'Online (Zoom Link Provided)',
            'max_capacity': 100,
            'owner_id': 'u1',
            'host_ids': ['u1', 'u2']
        },
        {
            'event_id': 'e2',
            'slug': 'advanced-dynamodb-deep-dive',
            'title': 'Advanced DynamoDB Deep Dive',
            'description': 'Explore advanced data modeling and optimization techniques in DynamoDB.',
            'start_at': '2025-08-15T09:00:00Z',
            'end_at': '2025-08-15T17:00:00Z',
            'venue': 'Saigon Exhibition and Convention Center',
            'max_capacity': 500,
            'owner_id': 'u2',
            'host_ids': ['u2']
        },
        {
            'event_id': 'e3',
            'slug': 'python-web-dev-meetup-september',
            'title': 'Python Web Dev Meetup - September Edition',
            'description': 'Monthly gathering for Python web developers to share knowledge and network.',
            'start_at': '2025-09-01T18:30:00Z',
            'end_at': '2025-09-01T20:30:00Z',
            'venue': 'Local Cafe, District 1',
            'max_capacity': 50,
            'owner_id': 'u1',
            'host_ids': ['u3']
        }
    ]
    for event in events_data: events_table.put_item(Item=event)
    print(f"Inserted {len(events_data)} events.")

    user_map = {u['user_id']: u for u in users_data}
    event_map = {e['event_id']: e for e in events_data}

    # Relations for Event e1
    relations_table.put_item(Item={
        'PK': f"USER#{user_map['u1']['user_id']}", 'SK': f"EVENT#{event_map['e1']['event_id']}#OWNER",
        'GSI1_PK': f"EVENT#{event_map['e1']['event_id']}", 'GSI1_SK': f"USER#{user_map['u1']['user_id']}#OWNER",
        'type': 'EventOwnership', 'user_id': user_map['u1']['user_id'], 'event_id': event_map['e1']['event_id'], 'role': 'owner',
        'first_name': user_map['u1']['first_name'], 'last_name': user_map['u1']['last_name'],
        'event_title': event_map['e1']['title'], 'event_date': event_map['e1']['start_at'] # Use title and start_at
    })
    relations_table.put_item(Item={
        'PK': f"USER#{user_map['u1']['user_id']}", 'SK': f"EVENT#{event_map['e1']['event_id']}#HOST",
        'GSI1_PK': f"EVENT#{event_map['e1']['event_id']}", 'GSI1_SK': f"USER#{user_map['u1']['user_id']}#HOST",
        'type': 'EventHosting', 'user_id': user_map['u1']['user_id'], 'event_id': event_map['e1']['event_id'], 'role': 'host',
        'first_name': user_map['u1']['first_name'], 'last_name': user_map['u1']['last_name'],
        'event_title': event_map['e1']['title'], 'event_date': event_map['e1']['start_at']
    })
    relations_table.put_item(Item={
        'PK': f"USER#{user_map['u2']['user_id']}", 'SK': f"EVENT#{event_map['e1']['event_id']}#HOST",
        'GSI1_PK': f"EVENT#{event_map['e1']['event_id']}", 'GSI1_SK': f"USER#{user_map['u2']['user_id']}#HOST",
        'type': 'EventHosting', 'user_id': user_map['u2']['user_id'], 'event_id': event_map['e1']['event_id'], 'role': 'host',
        'first_name': user_map['u2']['first_name'], 'last_name': user_map['u2']['last_name'],
        'event_title': event_map['e1']['title'], 'event_date': event_map['e1']['start_at']
    })

    # Relations for Event e2
    relations_table.put_item(Item={
        'PK': f"USER#{user_map['u2']['user_id']}", 'SK': f"EVENT#{event_map['e2']['event_id']}#OWNER",
        'GSI1_PK': f"EVENT#{event_map['e2']['event_id']}", 'GSI1_SK': f"USER#{user_map['u2']['user_id']}#OWNER",
        'type': 'EventOwnership', 'user_id': user_map['u2']['user_id'], 'event_id': event_map['e2']['event_id'], 'role': 'owner',
        'first_name': user_map['u2']['first_name'], 'last_name': user_map['u2']['last_name'],
        'event_title': event_map['e2']['title'], 'event_date': event_map['e2']['start_at']
    })
    relations_table.put_item(Item={
        'PK': f"USER#{user_map['u2']['user_id']}", 'SK': f"EVENT#{event_map['e2']['event_id']}#HOST",
        'GSI1_PK': f"EVENT#{event_map['e2']['event_id']}", 'GSI1_SK': f"USER#{user_map['u2']['user_id']}#HOST",
        'type': 'EventHosting', 'user_id': user_map['u2']['user_id'], 'event_id': event_map['e2']['event_id'], 'role': 'host',
        'first_name': user_map['u2']['first_name'], 'last_name': user_map['u2']['last_name'],
        'event_title': event_map['e2']['title'], 'event_date': event_map['e2']['start_at']
    })

    # Relations for Event e3
    relations_table.put_item(Item={
        'PK': f"USER#{user_map['u1']['user_id']}", 'SK': f"EVENT#{event_map['e3']['event_id']}#OWNER",
        'GSI1_PK': f"EVENT#{event_map['e3']['event_id']}", 'GSI1_SK': f"USER#{user_map['u1']['user_id']}#OWNER",
        'type': 'EventOwnership', 'user_id': user_map['u1']['user_id'], 'event_id': event_map['e3']['event_id'], 'role': 'owner',
        'first_name': user_map['u1']['first_name'], 'last_name': user_map['u1']['last_name'],
        'event_title': event_map['e3']['title'], 'event_date': event_map['e3']['start_at']
    })
    relations_table.put_item(Item={
        'PK': f"USER#{user_map['u3']['user_id']}", 'SK': f"EVENT#{event_map['e3']['event_id']}#HOST",
        'GSI1_PK': f"EVENT#{event_map['e3']['event_id']}", 'GSI1_SK': f"USER#{user_map['u3']['user_id']}#HOST",
        'type': 'EventHosting', 'user_id': user_map['u3']['user_id'], 'event_id': event_map['e3']['event_id'], 'role': 'host',
        'first_name': user_map['u3']['first_name'], 'last_name': user_map['u3']['last_name'],
        'event_title': event_map['e3']['title'], 'event_date': event_map['e3']['start_at']
    })
    print("Inserted relations data into UserEventRelations table.")

if __name__ == '__main__':
    create_all_tables()
    put_sample_data()
    print("\nDynamoDB table setup and data insertion complete.")