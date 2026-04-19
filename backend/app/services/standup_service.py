"""
Service layer for standup-related business logic.
Handles processing of standup inputs, voice transcripts, and AI-powered insights generation.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from ..models.standup import (
    StandupInput, StandupUpdate, VoiceTranscript,
    StandupSummary, StandupInsights, Blocker, ActionItem,
    VoiceProcessingResult
)

# Import AI services from the local package
try:
    from ..ai_services.summarization import SprintSummarizer
    from ..ai_services.blocker_detection import BlockerDetector
    from ..ai_services.voice_input import VoiceProcessor
    from ..ai_services.sentiment import SentimentAnalyzer
except ImportError:
    # Fallback for when ai_services are not available
    SprintSummarizer = None
    BlockerDetector = None
    VoiceProcessor = None
    SentimentAnalyzer = None

class StandupService:
    """
    Service class handling standup-related operations.
    Provides methods for processing standup inputs and generating AI insights.
    """

    def __init__(self):
        """Initialize AI service components."""
        self.summarizer = SprintSummarizer() if SprintSummarizer else None
        self.blocker_detector = BlockerDetector() if BlockerDetector else None
        self.voice_processor = VoiceProcessor() if VoiceProcessor else None
        self.sentiment_analyzer = SentimentAnalyzer() if SentimentAnalyzer else None

    def process_standup_input(self, standup_input: StandupInput) -> StandupInsights:
        """
        Process standup input and generate comprehensive insights.

        Args:
            standup_input: The standup data containing team updates

        Returns:
            StandupInsights: Complete insights including summary, blockers, and action items
        """
        updates = [update.dict() for update in standup_input.updates]

        # Generate summary
        summary = self._generate_summary(updates)

        # Detect blockers
        blockers = self._detect_blockers(updates)

        # Extract action items
        action_items = self._extract_action_items(updates)

        # Generate recommendations
        recommendations = self._generate_recommendations(summary, blockers)

        return StandupInsights(
            summary=summary,
            blockers=blockers,
            action_items=action_items,
            recommendations=recommendations
        )

    def process_voice_transcript(self, transcript: VoiceTranscript) -> VoiceProcessingResult:
        """
        Process voice transcript and extract structured information.

        Args:
            transcript: Voice transcript data (already converted to text)

        Returns:
            VoiceProcessingResult: Processed voice input with extracted information
        """
        if not self.voice_processor:
            return VoiceProcessingResult(
                success=False,
                error="Voice processing service not available",
                confidence=0.0
            )

        try:
            result = self.voice_processor.process_voice_transcript(
                transcript.transcript,
                {"person": transcript.person}
            )

            return VoiceProcessingResult(
                success=result.get("success", False),
                extracted_info=result.get("data", {}),
                confidence=result.get("data", {}).get("confidence", 0.0),
                summary=result.get("data", {}).get("summary")
            )
        except Exception as e:
            return VoiceProcessingResult(
                success=False,
                error=f"Voice processing failed: {str(e)}",
                confidence=0.0
            )

    def _generate_summary(self, updates: List[Dict[str, Any]]) -> StandupSummary:
        """
        Generate standup summary from updates.

        Args:
            updates: List of standup update dictionaries

        Returns:
            StandupSummary: Structured summary of the standup
        """
        if not self.summarizer:
            # Fallback summary generation
            return self._fallback_summary(updates)

        summary_data = self.summarizer.summarize_standup(updates)

        # Convert to our model format
        blockers = [
            Blocker(
                description=blocker.get("issue", "Blocker detected"),
                person=blocker.get("person", "Unknown"),
                severity="medium",  # Default severity
                category="general"
            )
            for blocker in summary_data.get("blockers", [])
        ]

        return StandupSummary(
            total_updates=summary_data.get("total_updates", len(updates)),
            completed_tasks=summary_data.get("completed_tasks", []),
            planned_tasks=summary_data.get("planned_tasks", []),
            blockers=blockers,
            key_insights=summary_data.get("key_insights", [])
        )

    def _detect_blockers(self, updates: List[Dict[str, Any]]) -> List[Blocker]:
        """
        Detect blockers from standup updates.

        Args:
            updates: List of standup update dictionaries

        Returns:
            List[Blocker]: List of detected blockers
        """
        if not self.blocker_detector:
            return []

        detected_blockers = self.blocker_detector.detect_blockers(updates)

        return [
            Blocker(
                description=blocker.get("description", ""),
                person=blocker.get("person", "Unknown"),
                severity=blocker.get("severity", "medium"),
                category=blocker.get("category", "general"),
                solution_hints=blocker.get("solution_hints", [])
            )
            for blocker in detected_blockers
        ]

    def _extract_action_items(self, updates: List[Dict[str, Any]]) -> List[ActionItem]:
        """
        Extract action items from standup updates.

        Args:
            updates: List of standup update dictionaries

        Returns:
            List[ActionItem]: List of extracted action items
        """
        action_items = []

        # Simple rule-based extraction
        action_keywords = ["need to", "will", "plan to", "should", "must", "todo", "action"]

        for update in updates:
            text = update.get("update", "").lower()
            person = update.get("person", "Unknown")

            # Check for action item patterns
            if any(keyword in text for keyword in action_keywords):
                # Extract potential action item
                sentences = text.split('.')
                for sentence in sentences:
                    if any(keyword in sentence for keyword in action_keywords):
                        action_items.append(ActionItem(
                            description=sentence.strip().capitalize(),
                            assignee=person,
                            priority="medium"
                        ))
                        break

        return action_items

    def _generate_recommendations(self, summary: StandupSummary, blockers: List[Blocker]) -> List[str]:
        """
        Generate recommendations based on summary and blockers.

        Args:
            summary: Standup summary
            blockers: List of detected blockers

        Returns:
            List[str]: List of recommendations
        """
        recommendations = []

        # Blocker-based recommendations
        if blockers:
            high_severity = [b for b in blockers if b.severity == "high"]
            if high_severity:
                recommendations.append("Address high-severity blockers immediately to prevent sprint delays")
            else:
                recommendations.append("Monitor identified blockers and provide support as needed")

        # Progress-based recommendations
        if summary.completed_tasks:
            recommendations.append(f"Great progress with {len(summary.completed_tasks)} completed tasks - maintain momentum")

        if not summary.planned_tasks:
            recommendations.append("Consider planning specific tasks for the next period to maintain velocity")

        # Team size consideration
        if summary.total_updates > 10:
            recommendations.append("Large team detected - consider breaking into smaller sub-teams for more focused standups")

        return recommendations

    def _fallback_summary(self, updates: List[Dict[str, Any]]) -> StandupSummary:
        """
        Fallback summary generation when AI services are not available.

        Args:
            updates: List of standup update dictionaries

        Returns:
            StandupSummary: Basic summary without AI processing
        """
        return StandupSummary(
            total_updates=len(updates),
            completed_tasks=[],
            planned_tasks=[],
            blockers=[],
            key_insights=["AI services not available - basic processing only"],
            action_items=[]
        )
