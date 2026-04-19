from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Task(BaseModel):
    id: int
    title: str
    status: str  # todo, in_progress, done, blocked
    assignee: Optional[str] = None
    points: Optional[int] = None

class SprintBase(BaseModel):
    name: str
    start_date: str
    end_date: str
    goal: str

class SprintCreate(SprintBase):
    pass

class SprintUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    goal: Optional[str] = None
    status: Optional[str] = None

class Sprint(SprintBase):
    id: int
    status: str = "active"
    tasks: List[Task] = []
