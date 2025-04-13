from pydantic import BaseModel, Field as PydanticField
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel
from typing import List

from models.user import User


class RoleBase(SQLModel):
    name: str = Field(index=True)
    description: str | None = None


class Role(RoleBase, table=True):
    __tablename__ = "role"
    __table_args__ = (
        UniqueConstraint("name", name="uq_role_name"),
        {
            'extend_existing': True
        }
    )

    id: int | None = Field(default=None, primary_key=True)

    users: List[User] = Relationship(back_populates="role")


class RoleCreate(RoleBase):
     model_config = {
        "json_schema_extra": {
            "examples": [
                { "name": "Project Manager", "description": "Manages project lifecycle." },
                { "name": "Developer", "description": "Develops software features." },
                { "name": "Analyst", "description": "Analyzes requirements and data." }
            ]
        }
    }


class RoleUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Project Manager",
                    "description": "Manages project lifecycle." 
                }
            ]
        }
    }


class RolePublic(BaseModel):
    id: int = PydanticField(validation_alias='id')
    name: str = PydanticField(validation_alias='name')
    description: str = PydanticField(validation_alias='description')

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Project Manager",
                    "description": "Manages project lifecycle."
                }
            ]
        },
        "from_attributes": True
    }
