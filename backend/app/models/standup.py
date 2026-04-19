"""
Pydantic models for standup-related data structures.
Defines request/response models for standup input and processing.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class StandupUpdate(BaseModel):
    """
    Individual standup update from a team member.
    Contains the person's update text and metadata.
    """
    person: str = Field(..., description="Name of the team member")
    update: str = Field(..., description="The standup update text")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="When the update was made")

class StandupInput(BaseModel):
    """
    Input model for standup data submission.
    Contains all updates from the daily standup.
    """
    updates: List[StandupUpdate] = Field(..., description="List of standup updates from team members")
    sprint_id: Optional[int] = Field(None, description="Associated sprint ID")
    team_id: Optional[str] = Field(None, description="Team identifier")

class VoiceTranscript(BaseModel):
    """
    Model for voice transcript input (already converted to text).
    Contains the transcribed text and optional metadata.
    """
    transcript: str = Field(..., description="The transcribed voice input")
    person: Optional[str] = Field(None, description="Name of the person who provided the voice input")
    confidence: Optional[float] = Field(None, description="Transcription confidence score (0-1)")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="When the transcript was created")

class Blocker(BaseModel):
    """
    Model representing a detected blocker.
    Contains blocker details and metadata.
    """
    description: str = Field(..., description="Description of the blocker")
    person: str = Field(..., description="Person affected by the blocker")
    severity: str = Field(..., description="Blocker severity: low, medium, high")
    category: Optional[str] = Field(None, description="Blocker category (technical, dependency, etc.)")
    solution_hints: Optional[List[str]] = Field(default_factory=list, description="Potential solution suggestions")

class ActionItem(BaseModel):
    """
    Model for action items extracted from standup or insights.
    Represents tasks that need to be completed.
    """
    description: str = Field(..., description="Action item description")
    assignee: Optional[str] = Field(None, description="Person responsible for the action item")
    priority: str = Field("medium", description="Priority level: low, medium, high")
    due_date: Optional[str] = Field(None, description="Due date for completion")
    status: str = Field("pending", description="Current status: pending, in_progress, completed")

class StandupSummary(BaseModel):
    """
    Summary of standup updates with key insights.
    Contains processed information from standup input.
    """
    total_updates: int = Field(..., description="Total number of standup updates")
    completed_tasks: List[str] = Field(default_factory=list, description="Tasks completed since last standup")
    planned_tasks: List[str] = Field(default_factory=list, description="Tasks planned for current period")
    blockers: List[Blocker] = Field(default_factory=list, description="Detected blockers")
    key_insights: List[str] = Field(default_factory=list, description="Key insights from the standup")
    action_items: List[ActionItem] = Field(default_factory=list, description="Extracted action items")
    sentiment: Optional[str] = Field(None, description="Overall team sentiment")

class StandupInsights(BaseModel):
    """
    Complete insights response containing summary, blockers, and action items.
    This is the main response model for insights endpoints.
    """
    summary: StandupSummary = Field(..., description="Standup summary with key information")
    blockers: List[Blocker] = Field(default_factory=list, description="Detailed list of detected blockers")
    action_items: List[ActionItem] = Field(default_factory=list, description="Action items to be addressed")
    recommendations: List[str] = Field(default_factory=list, description="AI-generated recommendations")
    processed_at: datetime = Field(default_factory=datetime.now, description="When insights were generated")

class VoiceProcessingResult(BaseModel):
    """
    Result of processing voice transcript input.
    Contains extracted information and confidence metrics.
    """
    success: bool = Field(..., description="Whether processing was successful")
    extracted_info: Dict[str, Any] = Field(default_factory=dict, description="Extracted structured information")
    confidence: float = Field(..., description="Overall processing confidence (0-1)")
    summary: Optional[str] = Field(None, description="Human-readable summary of the voice input")
    error: Optional[str] = Field(None, description="Error message if processing failed")
