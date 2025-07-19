# InnovationX_CRM

This is the repository for a CRM built by InnovationX.

## Data Model

- **Users Table**: Stores user profiles (ID, name, email, etc.)
- **Events Table**: Stores event details (ID, name, date, etc.)
- **UserEventRelations Table**: Maps users to events and their roles (host, attendee, etc.)

## Data Model Details

### Users Table
- **user_id** (string, PK): Unique identifier for each user
- **name** (string): Full name of the user
- **email** (string): Email address
- **role** (string): User role (e.g., host, attendee)
- **created_at** (datetime): Account creation timestamp
- **other fields**: Custom attributes as needed

### Events Table
- **event_id** (string, PK): Unique identifier for each event
- **name** (string): Event name
- **date** (datetime): Event date
- **location** (string): Event location
- **host_id** (string): User ID of the event host
- **description** (string): Event description
- **other fields**: Custom attributes as needed

### UserEventRelations Table
- **relation_id** (string, PK): Unique identifier for the relation
- **user_id** (string, FK): Linked user
- **event_id** (string, FK): Linked event
- **role** (string): Role in event (host, attendee, etc.)
- **status** (string): Participation status (confirmed, invited, etc.)
- **other fields**: Custom attributes as needed

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
- `POST /users/filter`: Filter users with pagination
- `POST /users/filter_by`: Get users by hosted event count and role
- `POST /users/send_email`: Send a predefined email to a list of users

### Example Requests

#### Get User Profile
```bash
curl -X GET "http://localhost:8000/users/123"
```

#### Get Events for a User
```bash
curl -X GET "http://localhost:8000/users/123/events"
```

#### Filter Users
```bash
curl -X POST "http://localhost:8000/users/filter" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"role": "host"}, "limit": 10}'
```

#### Get Users by Hosted Event Count
```bash
curl -X POST "http://localhost:8000/users/filter_by?min_events=2&role=host"
```

#### Send Email to Multiple Users
```bash
curl -X POST "http://localhost:8000/users/send_email" \
  -H "Content-Type: application/json" \
  -d '{"user_ids": ["123", "456", "789"]}'
```

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