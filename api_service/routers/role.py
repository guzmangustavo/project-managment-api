from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.db import get_session
from models.role import RoleCreate, RolePublic, RoleUpdate
from models.message import MessageResponse, ErrorDetail
from services.role import RoleService


router = APIRouter(
    prefix="/role",
    tags=["role"],
)


@router.post(
    "/",
    response_model=RolePublic,
    status_code=200,
    responses={
        200: {
            "description": "Role created successfully",
            "model": RolePublic
        },
        500: {
            "description": "Error creating role",
            "model": ErrorDetail
        }
    }
)
def create_role(
    role: RoleCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new role.
    """
    role_service = RoleService(session=session)
    role = role_service.create_role(role)
    if not role:
        raise HTTPException(status_code=500, detail="Error creating role")
    return role


@router.get("/", response_model=List[RolePublic], status_code=200)
def read_roles(session: Session = Depends(get_session)):
    """
    Retrieve a list of roles.
    """
    role_service = RoleService(session=session)
    roles = role_service.get_roles()
    return roles


@router.get(
    "/{role_id}",
    response_model=RolePublic,
    status_code=200,
    responses={
        200: {
            "description": "Role retrieved successfully",
            "model": RolePublic
        },
        404: {
            "description": "Role not found",
            "model": ErrorDetail
        }
    }
)
def read_role(
    role_id: int,
    session: Session = Depends(get_session)
):
    """
    Retrieve a role by ID.
    """
    role_service = RoleService(session=session)
    role = role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.put(
    "/{role_id}",
    response_model=RolePublic,
    status_code=200,
    responses={
        200: {
            "description": "Role updated successfully",
            "model": RolePublic
        },
        400: {
            "description": "Role not found",
            "model": ErrorDetail
        }
    }
)
def update_role(
    role_id: int,
    role: RoleUpdate,
    session: Session = Depends(get_session)
):
    """
    Update a role by ID.
    """
    role_service = RoleService(session=session)
    updated_role = role_service.update_role(role_id, role)
    if not updated_role:
        raise HTTPException(status_code=400, detail="Role not found")
    return updated_role


@router.delete(
    "/{role_id}",
    response_model=MessageResponse,
    status_code=200,
    responses={
        200: {
            "description": "Role deleted successfully",
            "model": MessageResponse
        },
        400: {
            "description": "Role not found or with associated users",
            "model": ErrorDetail
        }
    }
)
def delete_role(
    role_id: int,
    session: Session = Depends(get_session)
):
    """
    Delete a role by ID.
    """
    role_service = RoleService(session=session)
    deleted_role = role_service.delete_role(id=role_id)
    if not deleted_role:
        raise HTTPException(status_code=400, detail="Role not found or with associated users")
    return {"message": "Role deleted successfully"}