from fastapi import APIRouter, HTTPException
from typing import List
from ..models.user_story import UserStory, UserStoryCreate, UserStoryUpdate

router = APIRouter()

# In-memory storage for demo purposes
# In production, use a database
backlog_db = [
    {
        "id": 1,
        "title": "Implement OAuth Login",
        "description": "As a user, I want to log in using Google account",
        "priority": "high",
        "story_points": 5,
        "status": "todo",
        "created_at": "2023-10-01T00:00:00Z"
    },
    {
        "id": 2,
        "title": "Dashboard UI Redesign",
        "description": "As a user, I want a better dashboard experience",
        "priority": "medium",
        "story_points": 8,
        "status": "in_progress",
        "created_at": "2023-10-02T00:00:00Z"
    }
]

@router.get("/", response_model=List[UserStory])
async def get_backlog():
    """Get all user stories in the backlog"""
    return backlog_db

@router.get("/{story_id}", response_model=UserStory)
async def get_user_story(story_id: int):
    """Get a specific user story by ID"""
    story = next((s for s in backlog_db if s["id"] == story_id), None)
    if not story:
        raise HTTPException(status_code=404, detail="User story not found")
    return story

@router.post("/", response_model=UserStory)
async def create_user_story(story: UserStoryCreate):
    """Create a new user story"""
    new_id = max(s["id"] for s in backlog_db) + 1 if backlog_db else 1
    new_story = {
        "id": new_id,
        **story.dict(),
        "status": "todo",
        "created_at": "2023-10-01T00:00:00Z"  # In production, use datetime.now()
    }
    backlog_db.append(new_story)
    return new_story

@router.put("/{story_id}", response_model=UserStory)
async def update_user_story(story_id: int, story_update: UserStoryUpdate):
    """Update an existing user story"""
    story = next((s for s in backlog_db if s["id"] == story_id), None)
    if not story:
        raise HTTPException(status_code=404, detail="User story not found")

    for key, value in story_update.dict(exclude_unset=True).items():
        story[key] = value

    return story

@router.delete("/{story_id}")
async def delete_user_story(story_id: int):
    """Delete a user story"""
    global backlog_db
    story = next((s for s in backlog_db if s["id"] == story_id), None)
    if not story:
        raise HTTPException(status_code=404, detail="User story not found")

    backlog_db = [s for s in backlog_db if s["id"] != story_id]
    return {"message": "User story deleted successfully"}

@router.post("/prioritize")
async def prioritize_backlog(stories: List[int] = None):
    """AI-powered backlog prioritization"""
    # Simple prioritization based on priority and story points
    # In a real implementation, this would use more sophisticated algorithms
    if stories:
        # Reorder based on provided story IDs
        prioritized = []
        for story_id in stories:
            story = next((s for s in backlog_db if s["id"] == story_id), None)
            if story:
                prioritized.append(story)
        backlog_db[:] = prioritized + [s for s in backlog_db if s["id"] not in stories]

    # Return prioritized backlog
    return {"message": "Backlog prioritized", "backlog": backlog_db}
