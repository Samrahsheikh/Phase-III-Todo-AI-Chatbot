import uuid
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True
    )
    email: str = Field(
        unique=True,
        index=True,
        max_length=255
    )
    name: Optional[str] = Field(
        default=None,
        max_length=255
    )
    hashed_password: str = Field(
        max_length=255
    )

    tasks: List["Task"] = Relationship(
        back_populates="owner"
    )
