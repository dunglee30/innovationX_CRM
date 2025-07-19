# InnovationX_CRM

This is the repository for a CRM built by InnovationX.

## Data Model

- **Users Table**: Stores user profiles (ID, name, email, etc.)
- **Events Table**: Stores event details (ID, name, date, etc.)
- **UserEventRelations Table**: Maps users to events and their roles (host, attendee, etc.)

## Data Model Details

### Users Table
| Field        | Type     | Description                                 |
|-------------|----------|---------------------------------------------|
| user_id     | string   | Unique identifier for the user               |
| first_name  | string   | User's first name                           |
| last_name   | string   | User's last name                            |
| phone_number| string   | User's phone number                         |
| email       | string   | User's email address (unique)               |
| avatar      | string   | URL to the user's avatar image (optional)   |
| gender      | string   | User's gender (optional)                    |
| job_title   | string   | User's job title (optional)                 |
| company     | string   | User's company (optional)                   |
| city        | string   | User's current city (optional)              |
| state       | string   | User's current state/province (optional)    |

### Events Table
| Field        | Type     | Description                                 |
|-------------|----------|---------------------------------------------|
| event_id    | string   | Unique identifier for the event              |
| slug        | string   | URL-friendly identifier for the event        |
| title       | string   | Title of the event                           |
| description | string   | Detailed description of the event (optional) |
| start_at    | string   | Start date and time (ISO 8601 format)        |
| end_at      | string   | End date and time (ISO 8601 format)          |
| venue       | string   | Location or platform                         |
| max_capacity| int      | Maximum number of attendees (optional)       |

### UserEventRelations Table
| Field        | Type     | Description                                 |
|-------------|----------|---------------------------------------------|
| PK          | string   | Partition key                               |
| SK          | string   | Sort key                                    |
| GSI1_PK     | string   | Global secondary index partition key         |
| GSI1_SK     | string   | Global secondary index sort key              |
| type        | string   | Relation type (e.g., "EventOwnership")      |
| user_id     | string   | Linked user                                 |
| role        | string   | Role in event (owner, host, attendee)        |
| first_name  | string   | User's first name (optional)                 |
| last_name   | string   | User's last name (optional)                  |
| phone_number| string   | User's phone number (optional)               |
| email       | string   | User's email address (optional)              |
| job_title   | string   | User's job title (optional)                  |
| company     | string   | User's company (optional)                    |
| city        | string   | User's city (optional)                       |
| state       | string   | User's state/province (optional)             |
| event_id    | string   | Linked event                                 |
| event_title | string   | Event title (optional)                       |
| event_date  | string   | Event date (optional)                        |

#### Global Secondary Indexes (GSI)
- **GSI1_PK-GSI1_SK-index**: Used for fast querying users/events by event or user.
- **role-user_event-index**: Used for fast querying users by role and event count (e.g., hosts).

#### List Item Models

**UserEventListItem**
| Field       | Type   | Description                |
|-------------|--------|----------------------------|
| event_id    | string | Event identifier           |
| event_title | string | Event title                |
| role        | string | Role in event              |
| event_date  | string | Event date (optional)      |

**EventUserListItem**
| Field       | Type   | Description                |
|-------------|--------|----------------------------|
| user_id     | string | User identifier            |
| first_name  | string | User's first name (optional)|
| last_name   | string | User's last name (optional) |
| role        | string | Role in event              |
| phone_number| string | User's phone number (optional)|
| email       | string | User's email (optional)    |
| job_title   | string | User's job title (optional)|
| company     | string | User's company (optional)  |
| city        | string | User's city (optional)     |
| state       | string | User's state (optional)    |

## Entity Relationships
- One user can host or attend many events
- One event can have many users (hosts, attendees)
- Relations table links users and events with roles/status

## Application Architecture

- **FastAPI** backend
- **DynamoDB** for data storage
- **Repository Pattern** for data access
- **Routers** for modular API endpoints
- **Utils** for pagination, filtering, and email sending
- **Docker** for containerization

## API Endpoints

### User Endpoints
- `GET /users/{user_id}`: Get user profile by ID
- `GET /users/{user_id}/events`: Get events associated with a user
- `POST /users/`: Filter users with pagination and sorting
- `GET /users/events_and_role`: Get users by hosted event count and role
- `POST /users/send_email`: Send a predefined email to a list of users
- `POST /users/create`: Create a new user
- `PUT /users/{user_id}`: Update a user
- `DELETE /users/{user_id}`: Delete a user

### Example Requests

#### Get User Profile
```bash
curl -X GET "http://localhost:8000/users/123"
```

#### Get Events for a User
```bash
curl -X GET "http://localhost:8000/users/123/events"
```

#### Filter Users (with sorting)
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": [{"field": "company", "value": "Company Name"}],
    "limit": 10,
    "sort_by": "first_name",
    "sort_order": "asc"
  }'
```

#### Get Users by Hosted Event Count and Role
```bash
curl -X GET "http://localhost:8000/users/events_and_role?min_events=2&role=host"
```

#### Send Email to Multiple Users
```bash
curl -X POST "http://localhost:8000/users/send_email" \
  -H "Content-Type: application/json" \
  -d '{"user_ids": ["123", "456", "789"]}'
```

#### Create a New User
```bash
curl -X POST "http://localhost:8000/users/create" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice",
    "last_name": "Smith",
    "phone_number": "+84123456789",
    "email": "alice@example.com"
  }'
```

#### Update a User
```bash
curl -X PUT "http://localhost:8000/users/123" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice",
    "last_name": "Smith",
    "phone_number": "+84123456789",
    "email": "alice@example.com"
  }'
```

#### Delete a User
```bash
curl -X DELETE "http://localhost:8000/users/123"
```

## Requirements

- **Python**: >=3.9
- **FastAPI**: >=0.70.0
- **boto3**: >=1.20.23
- **DynamoDB**: Local or AWS DynamoDB (tested with DynamoDB Local Docker image)

See `requirements.txt` for full Python package requirements.

## Environment Variables

See `.env` for configuration of DynamoDB, AWS, and Gmail SMTP credentials.

## Running Locally

### Option 1: Run with Python

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start DynamoDB Local in a Docker container:
   ```bash
   docker compose up dynamodb-local
   ```
4. Initialize the database tables:
   ```bash
   python db_setup.py
   ```
5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Access API docs at `http://localhost:8000/docs`

### Option 2: Run with Docker

1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
2. The API will be available at `http://localhost:8000`
3. Access API docs at `http://localhost:8000/docs`

## License

MIT License