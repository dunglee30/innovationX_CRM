# app/routers/events_router.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List 
from app.models.events import Event, EventRequest
from app.models.user_event import EventUserListItem
from app.repositories.events_repository import EventRepository
from app.repositories.user_event_repository import UserEventRelationsRepository
from app.dependencies import get_event_repo, get_user_event_relations_repo
from botocore.exceptions import ClientError
import uuid
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

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
        logger.debug(f"Retrieved event data for ID {event_id}: {event_data is None}")
        return Event(**event_data)
    except HTTPException as e:
        raise e
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
    except HTTPException as e:
        raise e
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

@router.post(
    "/create",
    response_model=Event,
    summary="Create a new event",
    description="Creates a new event in the Events table."
)
async def create_event(event: EventRequest, repo: EventRepository = Depends(get_event_repo)):
    try:
        event_data = event.dict()
        event_data["event_id"] = str(uuid.uuid4())
        repo.create_event(event_data)
        return Event(**event_data)
    except HTTPException as e:
        raise e
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

@router.put(
    "/{event_id}",
    response_model=Event,
    summary="Update an event",
    description="Updates an existing event in the Events table."
)
async def update_event(event_id: str, event: EventRequest, repo: EventRepository = Depends(get_event_repo)):
    try:
        logger.debug(f"Updating event with ID: {event_id} with data: {event.dict()}")
        updated_event = repo.update_event(event_id, event.dict())
        if not updated_event:
            raise HTTPException(status_code=404, detail=f"Event with ID '{event_id}' not found.")
        return Event(**updated_event)
    except HTTPException as e:
        raise e
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

@router.delete(
    "/{event_id}",
    summary="Delete an event",
    description="Deletes an event from the Events table."
)
async def delete_event(event_id: str, repo: EventRepository = Depends(get_event_repo)):
    try:
        repo.delete_event(event_id)
        return {"message": f"Event with ID '{event_id}' deleted successfully."}
    except HTTPException as e:
        raise e
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")