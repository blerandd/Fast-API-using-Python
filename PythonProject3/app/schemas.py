from enum import IntEnum
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field


class Priority(IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


TodoStatus = Literal["NEW", "IN_PROGRESS", "DONE"]


class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512)
    todo_description: str = Field(..., min_length=1, max_length=2000)
    priority: Priority = Priority.LOW
    status: TodoStatus = "NEW"
    due_date: Optional[datetime] = None


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512)
    todo_description: Optional[str] = Field(None, min_length=1, max_length=2000)
    priority: Optional[Priority] = None
    status: Optional[TodoStatus] = None
    due_date: Optional[datetime] = None


class TodoReplace(TodoBase):
    pass


class TodoStatusUpdate(BaseModel):
    status: TodoStatus


class TodoOut(TodoBase):
    todo_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoStats(BaseModel):
    total: int
    high: int
    medium: int
    low: int


class HealthOut(BaseModel):
    status: str


SortBy = Literal["todo_id", "todo_name", "priority", "status", "due_date", "created_at", "updated_at"]
OrderBy = Literal["asc", "desc"]
ExportFormat = Literal["json", "csv"]
