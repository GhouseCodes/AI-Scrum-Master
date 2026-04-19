"""
Router for standup-related API endpoints.
Handles standup input submission, voice transcript processing, and insights generation.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models.standup import (
    StandupInput, VoiceTranscript, StandupInsights,
    VoiceProcessingResult, StandupSummary, Blocker, ActionItem
)
from ..services.standup_service import StandupService

router = APIRouter()
standup_service = StandupService()

@router.post("/input", response_model=StandupInsights)
async def submit_standup_input(standup_input: StandupInput):
    """
    Submit standup input for processing and insights generation.

    This endpoint accepts standup updates from team members and returns
    comprehensive insights including summary, detected blockers, and action items.

    Args:
        standup_input: Standup data containing team member updates

    Returns:
        StandupInsights: Complete insights with summary, blockers, and recommendations

    Raises:
        HTTPException: If processing fails or input is invalid
    """
    try:
        if not standup_input.updates:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one standup update is required"
            )

        insights = standup_service.process_standup_input(standup_input)
        return insights

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process standup input: {str(e)}"
        )

@router.post("/voice", response_model=VoiceProcessingResult)
async def submit_voice_transcript(transcript: VoiceTranscript):
    """
    Submit voice transcript for processing.

    This endpoint accepts voice transcripts (already converted to text) and
    extracts structured information including tasks, blockers, and sentiment.

    Args:
        transcript: Voice transcript data with text and metadata

    Returns:
        VoiceProcessingResult: Processed voice input with extracted information

    Raises:
        HTTPException: If processing fails or transcript is invalid
    """
    try:
        if not transcript.transcript or not transcript.transcript.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transcript text is required and cannot be empty"
            )

        result = standup_service.process_voice_transcript(transcript)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process voice transcript: {str(e)}"
        )

@router.post("/insights", response_model=StandupInsights)
async def generate_insights(standup_input: StandupInput):
    """
    Generate insights from standup data.

    Alternative endpoint for insights generation that returns the same
    comprehensive analysis as the /input endpoint.

    Args:
        standup_input: Standup data containing team member updates

    Returns:
        StandupInsights: Complete insights with summary, blockers, and recommendations
    """
    # Reuse the same logic as submit_standup_input
    return await submit_standup_input(standup_input)

@router.get("/summary", response_model=StandupSummary)
async def get_standup_summary():
    """
    Get a sample standup summary structure.

    This endpoint returns an empty summary structure for API documentation
    and testing purposes. In a full implementation, this would retrieve
    stored summaries.

    Returns:
        StandupSummary: Empty summary structure with all fields
    """
    return StandupSummary(
        total_updates=0,
        completed_tasks=[],
        planned_tasks=[],
        blockers=[],
        key_insights=[],
        action_items=[]
    )

@router.get("/blockers", response_model=List[Blocker])
async def get_sample_blockers():
    """
    Get sample blocker structures.

    This endpoint returns empty blocker structures for API documentation
    and testing purposes.

    Returns:
        List[Blocker]: Empty list of blockers
    """
    return []

@router.get("/action-items", response_model=List[ActionItem])
async def get_sample_action_items():
    """
    Get sample action item structures.

    This endpoint returns empty action item structures for API documentation
    and testing purposes.

    Returns:
        List[ActionItem]: Empty list of action items
    """
    return []
