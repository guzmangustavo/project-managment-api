from pydantic import BaseModel, computed_field, Field as PydanticField
from sqlalchemy import Column, DateTime 
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from typing import List, Any, Optional

from models.project import UserProject


class UserBase(SQLModel):
    name: str
    position: str


class User(UserBase, table=True):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id: int | None = Field(default=None, primary_key=True)
    role_id: int = Field(nullable=False, foreign_key="role.id", index=True)
    creation_date: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now()
        )
    )

    role: Optional["Role"] = Relationship(back_populates="users")
    projects: List["Project"] = Relationship(back_populates="users", link_model=UserProject)


class UserCreate(UserBase):
    role_id: int
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Max Weber",
                    "position": "Software Engineer",
                    "role_id": 1
                }
            ]
        }
    }


class UserUpdate(SQLModel):
    name: Optional[str] = None
    position: Optional[str] = None
    role_id: Optional[int] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Max Weber",
                    "position": "Software Engineer",
                    "role_id": 1
                }
            ]
        }
    }


class UserPublic(BaseModel):
    user_id: int = PydanticField(validation_alias='id')
    full_name: str = PydanticField(validation_alias='name')
    job_title: str = PydanticField(validation_alias='position')
    role: Any = PydanticField(exclude=True)
    creation_date_internal: datetime = PydanticField(
        validation_alias='creation_date',
        exclude=True
    )

    @computed_field
    @property
    def role_name(self) -> Optional[str]:
        return self.role.name if self.role else None
    
    @computed_field
    @property
    def joined_at(self) -> str:
        """Returns the creation date as an ISO 8601 formatted string."""
        return self.creation_date_internal.isoformat()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 1,
                    "full_name": "Max Weber",
                    "job_title": "Software Engineer",
                    "role_name": "Project Manager",
                    "joined_at": "2023-10-01T12:00:00"
                }
            ]
        },
        "from_attributes": True
    }