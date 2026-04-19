from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()

# Mock analytics data
analytics_data = {
    "velocity": {
        "current": 24,
        "average": 22,
        "trend": "up"
    },
    "burndown": {
        "ideal": [32, 28.8, 25.6, 22.4, 19.2, 16, 12.8, 9.6, 6.4, 3.2, 0],
        "actual": [32, 29, 25, 22, 21, 18, 15, 14, 10, 8]
    },
    "completion_time": {
        "average_days": 4.2,
        "fastest": 1,
        "slowest": 8
    },
    "team_metrics": {
        "total_tasks": 32,
        "completed_tasks": 18,
        "in_progress": 10,
        "blocked": 4
    }
}

@router.get("/")
async def get_analytics() -> Dict[str, Any]:
    """Get overall analytics data including AI recommendations"""
    recommendations = await get_ai_recommendations()
    return {
        **analytics_data,
        "recommendations": recommendations
    }

@router.get("/sprint/{sprint_id}")
async def get_sprint_analytics(sprint_id: int) -> Dict[str, Any]:
    """Get analytics for a specific sprint"""
    # In a real app, this would query the database for sprint-specific data
    return {
        **analytics_data,
        "sprint_id": sprint_id,
        "sprint_name": f"Sprint {sprint_id}"
    }

@router.get("/velocity")
async def get_velocity_trends() -> Dict[str, Any]:
    """Get team velocity trends over time"""
    return {
        "data": [
            {"sprint": "Sprint 5", "points": 18},
            {"sprint": "Sprint 6", "points": 22},
            {"sprint": "Sprint 7", "points": 20},
            {"sprint": "Sprint 8", "points": 24},
            {"sprint": "Sprint 9", "points": 23},
            {"sprint": "Sprint 10", "points": 25},
            {"sprint": "Sprint 11", "points": 27}
        ]
    }

@router.get("/burndown/{sprint_id}")
async def get_burndown_data(sprint_id: int) -> Dict[str, Any]:
    """Get burndown chart data for a sprint"""
    return analytics_data["burndown"]

@router.get("/completion-time")
async def get_completion_time_analytics() -> Dict[str, Any]:
    """Get task completion time analytics"""
    return analytics_data["completion_time"]

@router.get("/recommendations")
async def get_ai_recommendations() -> Dict[str, Any]:
    """Get AI-generated recommendations based on analytics"""
    return {
        "recommendations": [
            {
                "type": "sprint_length",
                "title": "Sprint Length Optimization",
                "description": "Based on past performance, your team may benefit from 3-week sprints instead of 2 weeks.",
                "confidence": 0.85
            },
            {
                "type": "workload",
                "title": "Workload Distribution",
                "description": "Consider redistributing tasks to balance team capacity.",
                "confidence": 0.72
            },
            {
                "type": "blockers",
                "title": "Blocker Resolution",
                "description": "Address recurring blockers to improve velocity.",
                "confidence": 0.91
            }
        ]
    }
