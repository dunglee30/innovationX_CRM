# app/routers/users_router.py

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.logger import logger
from typing import List
from app.models.users import User, UserRequest
from app.models.user_event import EventUserListItem, UserEventListItem
from app.repositories.users_repository import UserRepository
from app.repositories.user_event_repository import UserEventRelationsRepository
from app.dependencies import get_user_repo, get_user_event_relations_repo
from app.utils.pagination import paginate_dynamodb_response
from botocore.exceptions import ClientError, ParamValidationError
from app.utils.filter_request import FilterQueryRequest
from app.utils.email import send_email
import logging
import uuid

uvicorn_logger = logging.getLogger('uvicorn.error')
logger.handlers = uvicorn_logger.handlers
if __name__ != "main":
    logger.setLevel(uvicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "/",
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
            exclusive_start_key=query.exclusive_start_key,
            sort_by=query.sort_by,
            sort_order=query.sort_order
        )
        return paginate_dynamodb_response(response, User, query.limit)
    except HTTPException as e:
        raise e
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

@router.get(
    "/events_and_role",
    response_model=List[EventUserListItem],
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
        logger.debug(f"Querying for users with role '{role}' and at least {min_events} hosted events.")
        users = relations_repo.get_event_users_by_role_and_min_events(role=role, min_events=min_events)
        if not users or len(users) == 0:
            logger.warning(f"No users found with at least {min_events} '{role}'.")
            return []
        return [EventUserListItem(**item) for item in users]
    except HTTPException as e:
        raise e
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except ParamValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameters: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in get_users_by_hosted_event_count: {e}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")


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
    except HTTPException as e:
        raise e
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
    except HTTPException as e:
        raise e
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

@router.post(
    "/send_email",
    summary="Send Predefined Email to Multiple Users",
    description="Sends a predefined email to all specified users.",
)
async def send_email_to_users(
    user_ids: List[str],
    background_tasks: BackgroundTasks,
    repo: UserRepository = Depends(get_user_repo)
):
    """
    Sends a predefined email to all users in the given user_ids list.
    """
    subject = "Welcome to InnovationX CRM!"
    body = (
        "Dear user,\n\n"
        "Thank you for being a part of InnovationX CRM. "
        "We are excited to have you onboard.\n\n"
        "Best regards,\nInnovationX Team"
    )
    not_found = []
    sent_to = []
    for user_id in user_ids:
        user_data = repo.get_user_by_id(user_id)
        if not user_data or not user_data.get("email"):
            not_found.append(user_id)
            continue
        to_email = user_data["email"]
        background_tasks.add_task(send_email, to_email, subject, body)
        sent_to.append(to_email)
    return {
        "message": f"Emails will be sent to: {sent_to}",
        "not_found": not_found
    }

@router.post(
    "/create",
    response_model=User,
    summary="Create a new user",
    description="Creates a new user in the Users table."
)
async def create_user(user: UserRequest, repo: UserRepository = Depends(get_user_repo)):
    try:
        user_data = user.dict()
        user_data["user_id"] = str(uuid.uuid4())
        repo.create_user(user_data)
        return User(**user_data)
    except HTTPException as e:
        raise e
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

@router.put(
    "/{user_id}",
    response_model=User,
    summary="Update a user",
    description="Updates an existing user in the Users table."
)
async def update_user(user_id: str, user: UserRequest, repo: UserRepository = Depends(get_user_repo)):
    try:
        updated_user = repo.update_user(user_id, user.dict())
        if not updated_user:
            raise HTTPException(status_code=404, detail=f"User with ID '{user_id}' not found.")
        return User(**updated_user)
    except HTTPException as e:
        raise e
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

@router.delete(
    "/{user_id}",
    summary="Delete a user",
    description="Deletes a user from the Users table."
)
async def delete_user(user_id: str, repo: UserRepository = Depends(get_user_repo)):
    try:
        repo.delete_user(user_id)
        return {"message": f"User with ID '{user_id}' deleted successfully."}
    except HTTPException as e:
        raise e
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")