# from pymongo import ASCENDING
# from app.database.mongodb import mongo_db
#
# tasks_collection = mongo_db.get_collection("tasks")
# tasks_collection.create_index([("user_id", ASCENDING), ("status", ASCENDING)])

from pydantic import BaseModel, Field
from datetime import datetime
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
