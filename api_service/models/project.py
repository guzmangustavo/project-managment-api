import enum

from pydantic import BaseModel, computed_field, Field as PydanticField
from sqlalchemy import Column, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from typing import Any, List, Optional


class ProjectStatus(str, enum.Enum):
    PLANNING = "Planning"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"
    CANCELLED = "Cancelled"


class UserProject(SQLModel, table=True):
    __tablename__ = "user_project"
    user_id: int | None = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    project_id: int | None = Field(
        default=None, foreign_key="project.id", primary_key=True
    )


class ProjectBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None
    status: ProjectStatus = Field(
        default=ProjectStatus.PLANNING,
        sa_column=Column(SQLAlchemyEnum(ProjectStatus))
    )
    begin_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)


class Project(ProjectBase, table=True):
    __tablename__ = "project"
    __table_args__ = {'extend_existing': True}

    id: int | None = Field(default=None, primary_key=True)

    users: List["User"] = Relationship(back_populates="projects", link_model=UserProject)


class ProjectCreate(ProjectBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "New Super App",
                    "description": "Develop the next big thing.",
                    "status": "Planning",
                    "begin_date": "2024-01-15T09:00:00Z",
                    "end_date": "2024-12-20T17:00:00Z"
                }
            ]
        },
         "from_attributes": True
    }


class ProjectUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    begin_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "In Progress",
                    "description": "Development phase started."
                }
            ]
        }
    }


class ProjectPublic(BaseModel):
    project_id: int = PydanticField(validation_alias="id")
    name: str = PydanticField(validation_alias="name")
    description: Optional[str] = PydanticField(validation_alias="description")
    status: ProjectStatus = PydanticField(validation_alias="status")
    begin_date_internal: Optional[datetime] = PydanticField(validation_alias="begin_date", exclude=True)
    end_date_internal: Optional[datetime] = PydanticField(validation_alias="end_date", exclude=True)
    users: List[Any] = PydanticField(validation_alias="users", default_factory=list)

    @computed_field
    @property
    def begin_date(self) -> str:
        """Returns the begin date as an ISO 8601 formatted string."""
        return self.begin_date_internal.isoformat()

    @computed_field
    @property
    def end_date(self) -> str:
        """Returns the end date as an ISO 8601 formatted string."""
        return self.end_date_internal.isoformat()

    model_config = {
         "json_schema_extra": {
            "examples": [
                {
                    "project_id": 1,
                    "name": "Existing Project Alpha",
                    "description": "Maintenance phase.",
                    "status": "Completed",
                    "begin_date": "2023-01-10T09:00:00",
                    "end_date": "2023-11-30T17:00:00",
                }
            ]
        },
        "from_attributes": True
    }