from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.db import get_session
from models.message import MessageResponse, ErrorDetail
from models.project import ProjectCreate, ProjectPublic, ProjectUpdate
from services.project import ProjectService, UserProjectService


router = APIRouter(
    prefix="/project",
    tags=["project"],
)
@router.post(
    "/",
    response_model=ProjectPublic,
    status_code=200,
    responses={
        200: {
            "description": "Project created successfully",
            "model": ProjectPublic
        },
        500: {
            "description": "Error creating project",
            "model": ErrorDetail
        }
    }
)
def create_project(
    project: ProjectCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new project.
    """
    project_service = ProjectService(session=session)
    project = project_service.create_project(project)
    if not project:
        raise HTTPException(status_code=500, detail="Error creating project")
    return project


@router.get("/", response_model=List[ProjectPublic], status_code=200)
def read_projects(session: Session = Depends(get_session)):
    """
    Retrieve a list of projects.
    """
    project_service = ProjectService(session=session)
    projects = project_service.get_projects()
    return projects


@router.get(
    "/{project_id}",
    response_model=ProjectPublic,
    status_code=200,
    responses={
        200: {
            "description": "Project retrieved successfully",
            "model": ProjectPublic
        },
        404: {
            "description": "Project not found",
            "model": ErrorDetail
        }
    }
)
def read_project(
    project_id: int,
    session: Session = Depends(get_session)
):
    """
    Retrieve a project by its ID.
    """
    project_service = ProjectService(session=session)
    project = project_service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put(
    "/{project_id}",
    response_model=ProjectPublic,
    status_code=200,
    responses={
        200: {
            "description": "Project updated successfully",
            "model": ProjectPublic
        },
        400: {
            "description": "Project not found",
            "model": ErrorDetail
        }
    }
)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    session: Session = Depends(get_session)
):
    """
    Update a project by its ID.
    """
    project_service = ProjectService(session=session)
    project = project_service.update_project(project_id, project_update)
    if not project:
        raise HTTPException(status_code=400, detail="Project not found")
    return project


@router.delete(
    "/{project_id}",
    response_model=MessageResponse,
    status_code=200,
    responses={
        200: {
            "description": "Project deleted successfully",
            "model": MessageResponse
        },
        400: {
            "description": "Project not found",
            "model": ErrorDetail
        }
    }
)
def delete_project(
    project_id: int,
    session: Session = Depends(get_session)
):
    """
    Delete a project by its ID.
    """
    project_service = ProjectService(session=session)
    is_deleted = project_service.delete_project(project_id)
    if not is_deleted:
        raise HTTPException(status_code=400, detail="Project not found")
    return {"message": "Project deleted successfully"}


@router.post(
    "/{project_id}/user",
    response_model=MessageResponse,
    status_code=200,
    responses={
        200: {
            "description": "User added to project successfully",
            "model": MessageResponse
        },
        500: {
            "description": "Error adding user to project",
            "model": ErrorDetail
        }
    }
)
def add_user_to_project(
    project_id: int,
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    Add a user to a project.
    """
    user_project_service = UserProjectService(session=session)
    is_added = user_project_service.add_user_to_project(project_id, user_id)
    if not is_added:
        raise HTTPException(status_code=500, detail="Error adding user to project")
    return {"message": "User added to project successfully"}


@router.delete(
    "/{project_id}/user",
    response_model=MessageResponse,
    status_code=200,
    responses={
        200: {
            "description": "User removed from project successfully",
            "model": MessageResponse
        },
        500: {
            "description": "Error removing user from project",
            "model": ErrorDetail
        }
    }
)
def remove_user_from_project(
    project_id: int,
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    Remove a user from a project.
    """
    user_project_service = UserProjectService(session=session)
    is_removed = user_project_service.remove_user_from_project(project_id, user_id)
    if not is_removed:
        raise HTTPException(status_code=500, detail="Error removing user from project")
    return {"message": "User removed from project successfully"}