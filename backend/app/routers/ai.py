from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..ai_services import summarization, blocker_detection, sentiment, voice_input

router = APIRouter()

@router.post("/insights")
async def generate_insights(data: Dict[str, Any]):
    """Generate AI insights from team data"""
    try:
        updates = data.get('updates', [])
        sprint_data = data.get('sprint_data', {})

        # Summarize standup updates
        summarizer = summarization.SprintSummarizer()
        summary = summarizer.summarize_standup(updates)

        # Detect blockers
        detector = blocker_detection.BlockerDetector()
        blockers = detector.detect_blockers(updates)

        # Generate insights
        insights = []

        if summary['blockers']:
            insights.append(f"🚨 {len(summary['blockers'])} blocker(s) identified")

        if summary['completed_tasks']:
            insights.append(f"✅ {len(summary['completed_tasks'])} task(s) completed")

        if summary['planned_tasks']:
            insights.append(f"📋 {len(summary['planned_tasks'])} task(s) planned")

        return {
            "insights": insights,
            "summary": summary,
            "blockers": blockers,
            "recommendations": _generate_recommendations(summary, blockers)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")

@router.post("/sentiment")
async def analyze_sentiment(data: Dict[str, Any]):
    """Analyze sentiment in retrospective feedback"""
    try:
        feedback_items = data.get('feedback', [])

        analyzer = sentiment.SentimentAnalyzer()
        analysis = analyzer.analyze_retrospective_feedback(feedback_items)

        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")

@router.post("/blockers")
async def detect_blockers(data: Dict[str, Any]):
    """Detect blockers in team updates"""
    try:
        updates = data.get('updates', [])

        detector = blocker_detection.BlockerDetector()
        blockers = detector.detect_blockers(updates)

        return {"blockers": blockers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blocker detection failed: {str(e)}")

@router.post("/voice")
async def process_voice_input(data: Dict[str, Any]):
    """Process voice input transcript"""
    try:
        transcript = data.get('transcript', '')
        user_context = data.get('context', {})

        processor = voice_input.VoiceProcessor()
        result = processor.process_voice_transcript(transcript, user_context)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice processing failed: {str(e)}")

@router.post("/summarize")
async def summarize_content(data: Dict[str, Any]):
    """Summarize meeting notes or sprint data"""
    try:
        content_type = data.get('type', 'meeting')
        content = data.get('content', '')

        if content_type == 'meeting':
            summary = summarization.summarize_meeting_notes(content)
        else:
            # Assume sprint data
            sprint_data = data.get('sprint_data', {})
            summarizer = summarization.SprintSummarizer()
            summary = summarizer.summarize_sprint(sprint_data)

        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

def _generate_recommendations(summary: Dict[str, Any], blockers: List[Dict[str, Any]]) -> List[str]:
    """Generate recommendations based on summary and blockers"""
    recommendations = []

    if blockers:
        recommendations.append("Address identified blockers immediately")

    if summary.get('total_updates', 0) > 0:
        blocker_rate = len(blockers) / summary['total_updates']
        if blocker_rate > 0.3:
            recommendations.append("High blocker rate detected - consider team capacity issues")

    if summary.get('completed_tasks', []):
        recommendations.append("Continue momentum on completed tasks")

    if not recommendations:
        recommendations.append("Team is progressing well - maintain current practices")

    return recommendations
