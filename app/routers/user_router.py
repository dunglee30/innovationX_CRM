# app/routers/users_router.py

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.models.users import User
from app.models.user_event import UserEventListItem
from app.repositories.users_repository import UserRepository
from app.repositories.user_event_repository import UserEventRelationsRepository
from app.dependencies import get_user_repo, get_user_event_relations_repo
from app.utils.pagination import paginate_dynamodb_response
from botocore.exceptions import ClientError
from app.utils.filter_request import FilterQueryRequest
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

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

@router.get(
    "/by_role_event_count",
    response_model=List[User],
    summary="Get Users by Hosted Event Count",
    description="Retrieves users who have hosted at least the specified number of events.",
)
async def get_users_by_role_event_count(
    min_events: int = Query(1, description="Minimum number of hosted events"),
    role: str = Query("host", description="Role to filter users by"),
    relations_repo: UserEventRelationsRepository = Depends(get_user_event_relations_repo)
):
    """
    Retrieves users who have hosted at least min_events events.
    """
    try:
        users = relations_repo.get_event_users_by_role_and_min_events(role=role, min_events=min_events)
        if not users:
            raise HTTPException(status_code=404, detail=f"No users found with at least {min_events} hosted events.")
        return users
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        logger.error(f"Unexpected error in get_users_by_hosted_event_count: {e}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

@router.post(
    "/filter",
    summary="Get Users by Filter",
    response_model=dict,
    description="Retrieves users from the 'Users' table using a generic filter and pagination.",
)
async def get_users_by_filter(
    query: FilterQueryRequest,
    repo: UserRepository = Depends(get_user_repo)
):
    """
    Retrieves users using a generic filter and DynamoDB pagination.
    """
    try:
        response = repo.get_users_by_filter(
            query.filter,
            limit=query.limit,
            exclusive_start_key=query.exclusive_start_key
        )
        return paginate_dynamodb_response(response, User, query.limit)
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")