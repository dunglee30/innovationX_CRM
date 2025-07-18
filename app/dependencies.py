# app/dependencies.py
# Suitable for Python 3.9+
from app.repositories.users_repository import UserRepository
from app.repositories.events_repository import EventRepository
from app.repositories.user_event_repository import UserEventRelationsRepository

# Instantiate repositories here. FastAPI's Depends will provide these instances.
user_repo_instance = UserRepository()
event_repo_instance = EventRepository()
user_event_relations_repo_instance = UserEventRelationsRepository()

def get_user_repo() -> UserRepository:
    return user_repo_instance

def get_event_repo() -> EventRepository:
    return event_repo_instance

def get_user_event_relations_repo() -> UserEventRelationsRepository:
    return user_event_relations_repo_instance