from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=120,
        description="The title of the task"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="A detailed description of the task"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="The due date for the task"
    )
    priority: int = Field(
        default=2,
        ge=1,
        le=3,
        description="The priority level of the task (1-3)"
    )

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=120
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500
    )
    due_date: Optional[datetime] = None
    priority: Optional[int] = Field(
        default=None,
        ge=1,
        le=3
    )
    status: Optional[str] = None

class Task(TaskCreate):
    id: int = Field(..., description="Unique task ID")
    status: str = Field(default="open", description="Task status")
    created_at: datetime
    updated_at: datetime
