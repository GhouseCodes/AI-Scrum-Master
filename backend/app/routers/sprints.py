from fastapi import APIRouter, HTTPException
from typing import List
from ..models.sprint import Sprint, SprintCreate, SprintUpdate

router = APIRouter()

# In-memory storage for demo purposes
# In production, use a database
sprints_db = [
    {
        "id": 1,
        "name": "Sprint 12",
        "start_date": "2023-10-01",
        "end_date": "2023-10-14",
        "status": "active",
        "goal": "Implement core authentication flow",
        "tasks": [
            {"id": 1, "title": "Implement OAuth Login", "status": "todo", "assignee": "Alice", "points": 5},
            {"id": 2, "title": "Dashboard UI Redesign", "status": "in_progress", "assignee": "Bob", "points": 8},
            {"id": 3, "title": "API Rate Limiter", "status": "done", "assignee": "Charlie", "points": 3}
        ]
    }
]

@router.get("/", response_model=List[Sprint])
async def get_sprints():
    """Get all sprints"""
    return sprints_db

@router.get("/{sprint_id}", response_model=Sprint)
async def get_sprint(sprint_id: int):
    """Get a specific sprint by ID"""
    sprint = next((s for s in sprints_db if s["id"] == sprint_id), None)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint

@router.post("/", response_model=Sprint)
async def create_sprint(sprint: SprintCreate):
    """Create a new sprint"""
    new_id = max(s["id"] for s in sprints_db) + 1 if sprints_db else 1
    new_sprint = {
        "id": new_id,
        **sprint.dict(),
        "tasks": []
    }
    sprints_db.append(new_sprint)
    return new_sprint

@router.put("/{sprint_id}", response_model=Sprint)
async def update_sprint(sprint_id: int, sprint_update: SprintUpdate):
    """Update an existing sprint"""
    sprint = next((s for s in sprints_db if s["id"] == sprint_id), None)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")

    for key, value in sprint_update.dict(exclude_unset=True).items():
        sprint[key] = value

    return sprint

@router.delete("/{sprint_id}")
async def delete_sprint(sprint_id: int):
    """Delete a sprint"""
    global sprints_db
    sprint = next((s for s in sprints_db if s["id"] == sprint_id), None)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")

    sprints_db = [s for s in sprints_db if s["id"] != sprint_id]
    return {"message": "Sprint deleted successfully"}
