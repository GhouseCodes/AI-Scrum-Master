"""
Internal AI service for summarizing sprint data and meeting notes.
Uses rule-based algorithms instead of external APIs.
"""

import re
from typing import List, Dict, Any
from datetime import datetime

class SprintSummarizer:
    def __init__(self):
        self.keywords = {
            'blocker': ['blocked', 'blocking', 'stuck', 'issue', 'problem', 'cannot', 'unable'],
            'progress': ['completed', 'finished', 'done', 'implemented', 'merged', 'deployed'],
            'planning': ['will', 'plan', 'next', 'tomorrow', 'sprint', 'goal']
        }

    def summarize_standup(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize daily standup updates using rule-based analysis"""
        summary = {
            'total_updates': len(updates),
            'blockers': [],
            'completed_tasks': [],
            'planned_tasks': [],
            'key_insights': []
        }

        for update in updates:
            text = update.get('update', '').lower()

            # Detect blockers
            if any(keyword in text for keyword in self.keywords['blocker']):
                summary['blockers'].append({
                    'person': update.get('person', 'Unknown'),
                    'issue': self._extract_blocker(text)
                })

            # Detect completed tasks
            if any(keyword in text for keyword in self.keywords['progress']):
                summary['completed_tasks'].append({
                    'person': update.get('person', 'Unknown'),
                    'task': self._extract_task(text)
                })

            # Detect planned tasks
            if any(keyword in text for keyword in self.keywords['planning']):
                summary['planned_tasks'].append({
                    'person': update.get('person', 'Unknown'),
                    'task': self._extract_task(text)
                })

        # Generate insights
        summary['key_insights'] = self._generate_insights(summary)

        return summary

    def summarize_sprint(self, sprint_data: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize sprint progress"""
        tasks = sprint_data.get('tasks', [])
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.get('status') == 'done'])
        in_progress = len([t for t in tasks if t.get('status') == 'in_progress'])
        blocked = len([t for t in tasks if t.get('status') == 'blocked'])

        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return {
            'total_tasks': total_tasks,
            'completed': completed_tasks,
            'in_progress': in_progress,
            'blocked': blocked,
            'completion_rate': round(completion_rate, 1),
            'status': self._assess_sprint_health(completion_rate, blocked)
        }

    def _extract_blocker(self, text: str) -> str:
        """Extract blocker description from text"""
        # Simple extraction - in real implementation, use NLP
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence for keyword in self.keywords['blocker']):
                return sentence.strip()
        return "Blocker detected"

    def _extract_task(self, text: str) -> str:
        """Extract task description from text"""
        # Simple extraction - in real implementation, use NLP
        return text.strip()[:100] + "..." if len(text) > 100 else text.strip()

    def _generate_insights(self, summary: Dict[str, Any]) -> List[str]:
        """Generate insights based on summary data"""
        insights = []

        if summary['blockers']:
            insights.append(f"🚨 {len(summary['blockers'])} blocker(s) identified - immediate attention needed")

        if summary['completed_tasks']:
            insights.append(f"✅ {len(summary['completed_tasks'])} task(s) completed today")

        if summary['planned_tasks']:
            insights.append(f"📋 {len(summary['planned_tasks'])} task(s) planned for next period")

        # Velocity insights
        if summary['total_updates'] > 0:
            blocker_rate = len(summary['blockers']) / summary['total_updates']
            if blocker_rate > 0.3:
                insights.append("⚠️ High blocker rate detected - consider team capacity issues")

        return insights

    def _assess_sprint_health(self, completion_rate: float, blocked_count: int) -> str:
        """Assess overall sprint health"""
        if completion_rate >= 80 and blocked_count == 0:
            return "healthy"
        elif completion_rate >= 60 or blocked_count <= 2:
            return "warning"
        else:
            return "critical"

def summarize_meeting_notes(notes: str) -> Dict[str, Any]:
    """Summarize meeting notes using internal algorithms"""
    summarizer = SprintSummarizer()

    # Split notes into sections
    sections = re.split(r'\n\s*\n', notes)

    summary = {
        'total_sections': len(sections),
        'key_points': [],
        'action_items': [],
        'decisions': []
    }

    for section in sections:
        lines = section.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Detect action items
            if re.match(r'^[-*•]\s*(todo|action|assign|follow)', line.lower()):
                summary['action_items'].append(line)

            # Detect decisions
            elif re.match(r'^[-*•]\s*(decided|decision|agreed)', line.lower()):
                summary['decisions'].append(line)

            # Key points
            else:
                summary['key_points'].append(line[:200] + "..." if len(line) > 200 else line)

    return summary
