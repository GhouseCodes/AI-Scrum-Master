from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserStoryBase(BaseModel):
    title: str
    description: str
    priority: str  # low, medium, high
    story_points: Optional[int] = None

class UserStoryCreate(UserStoryBase):
    pass

class UserStoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    story_points: Optional[int] = None
    status: Optional[str] = None

class UserStory(UserStoryBase):
    id: int
    status: str = "todo"
    created_at: str
