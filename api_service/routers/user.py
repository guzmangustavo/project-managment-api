from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session
from typing import List

from core.db import get_session
from models.user import UserCreate, UserPublic, UserUpdate
from models.message import MessageResponse, ErrorDetail
from services.user import UserService


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post(
    "/", 
    response_model=UserPublic,
    status_code=200,
    responses={
        200: {
            "description": "User created successfully",
            "model": UserPublic
        },
        500: {
            "description": "Error creating user",
            "model": ErrorDetail
        }
    }
)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_session)
) -> UserPublic:
    """
    Create a new user.
    """
    user_service = UserService(session=session)
    user = user_service.create_user(user)
    if not user:
        raise HTTPException(status_code=500, detail="Error creating user")
    return user


@router.get("/", response_model=List[UserPublic], status_code=200)
def read_users(session: Session = Depends(get_session)) -> List[UserPublic]:
    """
    Retrieve a list of users.
    """
    user_service = UserService(session=session)
    users = user_service.get_users()
    return users


@router.get(
    "/{user_id}",
    response_model=UserPublic,
    status_code=200,
    responses={
        200: {
            "description": "User queried successfully",
            "model": UserPublic
        },
        404: {
            "description": "User not found",
            "model": ErrorDetail
        }
    }
)
def read_user(
    user_id: int,
    session: Session = Depends(get_session)
) -> UserPublic:
    """
    Retrieve a single user by its ID.
    """
    user_service = UserService(session=session)
    user = user_service.get_user_by_id(id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put(
    "/{user_id}",
    response_model=UserPublic,
    status_code=200, 
    responses={
        200: {
            "description": "User updated successfully",
            "model": UserPublic
        },
        400: {
            "description": "User not found or update failed",
            "model": ErrorDetail
        }
    }
)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session)
) -> UserPublic:
    """
    Update an existing user by its ID.
    Only fields provided in the request body will be updated.
    """
    user_service = UserService(session=session)
    updated_user = user_service.update_user(id=user_id, user_update=user_update)
    if updated_user is None:
        raise HTTPException(status_code=400, detail="User not found or update failed")
    return updated_user


@router.delete(
    "/{user_id}", 
    status_code=200, 
    responses={
        200: {
            "description": "User deleted successfully",
            "model": MessageResponse
        },
        400: {
            "description": "User not found",
            "model": ErrorDetail
        },
        500: {
            "description": "Error deleting user",
            "model": ErrorDetail
        }
    }
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session)
) -> MessageResponse:
    """
    Delete a user by its ID.
    """
    user_service = UserService(session=session)
    is_deleted = user_service.delete_user(id=user_id)

    if is_deleted is None:
        raise HTTPException(status_code=400, detail="User not found")
    elif is_deleted is False:
        raise HTTPException(status_code=500, detail="Error deleting user")
    else:
        return MessageResponse(
            message=f"User with id {user_id} deleted successfully"
        )