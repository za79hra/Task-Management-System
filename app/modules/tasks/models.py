from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Priority(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'


class TaskStatus(str, Enum):
    pending = 'pending'
    running = 'running'
    finished = 'finished'
    error = 'error'


class TaskBase(BaseModel):
    title: str
    description: str = None
    priority: Optional[Priority] = Field(...)
    status: Optional[TaskStatus] = Field(...)
    assigned_user_id: Optional[int] = None
