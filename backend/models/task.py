import uuid
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Task(SQLModel, table=True):
    __tablename__ = "task"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True
    )
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

    owner_id: uuid.UUID = Field(
        foreign_key="user.id",
        index=True
    )

    owner: Optional["User"] = Relationship(
        back_populates="tasks"
    )
