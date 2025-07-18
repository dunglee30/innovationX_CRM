# app/routers/events_router.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List # Use typing.List for Python 3.9 compatibility
from app.models.events import Event
from app.models.user_event import EventUserListItem
from app.repositories.events_repository import EventRepository
from app.repositories.user_event_repository import UserEventRelationsRepository
from app.dependencies import get_event_repo, get_user_event_relations_repo
from botocore.exceptions import ClientError

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.get(
    "/{event_id}",
    response_model=Event,
    summary="Get Event Details by ID",
    description="Retrieves an event's details from the 'Events' table.",
)
async def get_event(event_id: str, repo: EventRepository = Depends(get_event_repo)):
    """
    Retrieves an event's details from the Events table.
    """
    try:
        event_data = repo.get_event_by_id(event_id)
        if not event_data:
            raise HTTPException(status_code=404, detail=f"Event with ID '{event_id}' not found.")
        return Event(**event_data)
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

@router.get(
    "/{event_id}/users",
    response_model=List[EventUserListItem], # Use typing.List
    summary="Get Users for an Event",
    description="Retrieves all users (owner, hosts) associated with a specific event from the 'UserEventRelations' table via GSI.",
)
async def get_event_associated_users(
    event_id: str, 
    repo: UserEventRelationsRepository = Depends(get_user_event_relations_repo)
):
    """
    Retrieves users associated with an event using the UserEventRelations GSI.
    """
    try:
        users_data = repo.get_users_for_event(event_id)
        return [EventUserListItem(**item) for item in users_data]
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")