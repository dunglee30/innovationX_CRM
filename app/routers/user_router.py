# app/routers/users_router.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List # Use typing.List for Python 3.9 compatibility
from app.models.users import User
from app.models.user_event import UserEventListItem
from app.repositories.users_repository import UserRepository
from app.repositories.user_event_repository import UserEventRelationsRepository
from app.dependencies import get_user_repo, get_user_event_relations_repo
from botocore.exceptions import ClientError

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get(
    "/{user_id}",
    response_model=User,
    summary="Get User Profile by ID",
    description="Retrieves a user's full profile details from the 'Users' table.",
)
async def get_user(user_id: str, repo: UserRepository = Depends(get_user_repo)):
    """
    Retrieves a user's profile from the Users table.
    """
    try:
        user_data = repo.get_user_by_id(user_id)
        if not user_data:
            raise HTTPException(status_code=404, detail=f"User with ID '{user_id}' not found.")
        return User(**user_data)
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

@router.get(
    "/{user_id}/events",
    response_model=List[UserEventListItem], # Use typing.List
    summary="Get Events for a User",
    description="Retrieves all events (owned, hosted) associated with a specific user from the 'UserEventRelations' table.",
)
async def get_user_associated_events(
    user_id: str, 
    repo: UserEventRelationsRepository = Depends(get_user_event_relations_repo)
):
    """
    Retrieves events associated with a user using the UserEventRelations table.
    """
    try:
        events_data = repo.get_events_for_user(user_id)
        return [UserEventListItem(**item) for item in events_data]
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")