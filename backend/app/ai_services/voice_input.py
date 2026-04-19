"""
Internal voice input processing service.
Uses Web Speech API on frontend, processes text on backend with rule-based analysis.
No external APIs required.
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime

class VoiceProcessor:
    def __init__(self):
        # Keywords for different types of scrum updates
        self.update_keywords = {
            'completed': ['completed', 'finished', 'done', 'implemented', 'merged', 'deployed', 'delivered'],
            'in_progress': ['working on', 'currently', 'in progress', 'started', 'began'],
            'blocked': ['blocked', 'stuck', 'issue', 'problem', 'waiting', 'cannot proceed'],
            'planned': ['will', 'plan to', 'next', 'tomorrow', 'sprint', 'goal', 'planning']
        }

        # Task-related keywords
        self.task_indicators = [
            'task', 'story', 'feature', 'bug', 'issue', 'ticket',
            'implement', 'fix', 'add', 'create', 'update', 'refactor'
        ]

    def process_voice_transcript(self, transcript: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process voice transcript and extract structured information"""
        transcript = transcript.lower().strip()

        # Basic validation
        if not transcript or len(transcript) < 10:
            return {
                'success': False,
                'error': 'Transcript too short or empty',
                'confidence': 0.0
            }

        # Extract structured information
        extracted_info = {
            'original_transcript': transcript,
            'update_type': self._classify_update_type(transcript),
            'mentioned_tasks': self._extract_tasks(transcript),
            'blockers': self._detect_blockers(transcript),
            'sentiment': self._analyze_sentiment(transcript),
            'key_phrases': self._extract_key_phrases(transcript),
            'confidence': self._calculate_confidence(transcript),
            'timestamp': datetime.now().isoformat(),
            'user_context': user_context
        }

        # Generate summary
        extracted_info['summary'] = self._generate_summary(extracted_info)

        return {
            'success': True,
            'data': extracted_info
        }

    def _classify_update_type(self, transcript: str) -> str:
        """Classify the type of scrum update"""
        scores = {}

        for update_type, keywords in self.update_keywords.items():
            score = sum(1 for keyword in keywords if keyword in transcript)
            scores[update_type] = score

        # Return the type with highest score, default to 'general'
        if max(scores.values()) > 0:
            return max(scores.keys(), key=lambda k: scores[k])
        else:
            return 'general'

    def _extract_tasks(self, transcript: str) -> List[str]:
        """Extract mentioned tasks or work items"""
        tasks = []

        # Split into sentences
        sentences = re.split(r'[.!?]+', transcript)

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check if sentence mentions a task
            if any(indicator in sentence for indicator in self.task_indicators):
                # Clean up the task description
                task = self._clean_task_description(sentence)
                if task:
                    tasks.append(task)

        return tasks

    def _detect_blockers(self, transcript: str) -> List[str]:
        """Detect any blockers mentioned in the transcript"""
        blockers = []

        # Look for blocker patterns
        blocker_patterns = [
            r'blocked by (.+?)(?:\.|$)',
            r'stuck (?:on|with) (.+?)(?:\.|$)',
            r'cannot (?:proceed|continue) (?:because|due to) (.+?)(?:\.|$)',
            r'waiting (?:for|on) (.+?)(?:\.|$)',
            r'issue (?:with|is) (.+?)(?:\.|$)',
            r'problem (?:with|is) (.+?)(?:\.|$)'        ]

        for pattern in blocker_patterns:
            matches = re.findall(pattern, transcript, re.IGNORECASE)
            blockers.extend(matches)

        # Remove duplicates and clean
        blockers = list(set(blockers))
        blockers = [self._clean_blocker_description(b) for b in blockers if b.strip()]

        return blockers

    def _analyze_sentiment(self, transcript: str) -> str:
        """Simple sentiment analysis for voice input"""
        positive_words = ['good', 'great', 'excellent', 'happy', 'pleased', 'successful', 'completed']
        negative_words = ['bad', 'terrible', 'frustrated', 'stuck', 'blocked', 'issue', 'problem']

        positive_count = sum(1 for word in positive_words if word in transcript)
        negative_count = sum(1 for word in negative_words if word in transcript)

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

    def _extract_key_phrases(self, transcript: str) -> List[str]:
        """Extract key phrases from the transcript"""
        # Simple extraction of noun phrases and important terms
        words = re.findall(r'\b\w+\b', transcript)

        # Filter for potentially important words (longer than 4 chars)
        key_words = [word for word in words if len(word) > 4 and word not in {
            'about', 'would', 'there', 'their', 'which', 'could', 'should', 'these', 'those'
        }]

        # Return top 5 most frequent key words
        from collections import Counter
        word_counts = Counter(key_words)
        return [word for word, count in word_counts.most_common(5)]

    def _calculate_confidence(self, transcript: str) -> float:
        """Calculate confidence score for the processing"""
        # Simple confidence based on transcript length and clarity
        word_count = len(re.findall(r'\b\w+\b', transcript))

        # Base confidence
        confidence = 0.5

        # Length factor
        if word_count < 5:
            confidence -= 0.3
        elif word_count > 20:
            confidence += 0.2

        # Clarity factors
        if self._classify_update_type(transcript) != 'general':
            confidence += 0.1
        if self._extract_tasks(transcript):
            confidence += 0.1
        if self._detect_blockers(transcript):
            confidence += 0.1

        return max(0.0, min(1.0, confidence))

    def _generate_summary(self, extracted_info: Dict[str, Any]) -> str:
        """Generate a human-readable summary"""
        update_type = extracted_info['update_type']
        tasks = extracted_info['mentioned_tasks']
        blockers = extracted_info['blockers']
        sentiment = extracted_info['sentiment']

        summary_parts = []

        if update_type != 'general':
            summary_parts.append(f"Update type: {update_type.replace('_', ' ')}")

        if tasks:
            summary_parts.append(f"Tasks mentioned: {', '.join(tasks[:3])}")

        if blockers:
            summary_parts.append(f"Blockers identified: {', '.join(blockers[:2])}")

        if sentiment != 'neutral':
            summary_parts.append(f"Overall sentiment: {sentiment}")

        if not summary_parts:
            summary_parts.append("General update recorded")

        return ". ".join(summary_parts)

    def _clean_task_description(self, text: str) -> str:
        """Clean and normalize task description"""
        # Remove common prefixes
        text = re.sub(r'^(?:i am |i\'m |working on |started |finished |completed )\s*', '', text, flags=re.IGNORECASE)

        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:]

        # Limit length
        if len(text) > 100:
            text = text[:97] + "..."

        return text.strip()

    def _clean_blocker_description(self, text: str) -> str:
        """Clean blocker description"""
        # Remove extra whitespace
        text = ' '.join(text.split())

        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:]

        return text.strip()

    def validate_transcript_quality(self, transcript: str) -> Dict[str, Any]:
        """Validate the quality of a voice transcript"""
        quality_metrics = {
            'length_score': min(len(transcript.split()) / 20, 1.0),  # Optimal: 20+ words
            'clarity_score': 1.0 if re.search(r'[.!?]', transcript) else 0.5,  # Has punctuation
            'content_score': 1.0 if len(re.findall(r'\b\w{4,}\b', transcript)) > 3 else 0.3,  # Has substantial words
            'structure_score': 1.0 if self._classify_update_type(transcript) != 'general' else 0.5
        }

        overall_quality = sum(quality_metrics.values()) / len(quality_metrics)

        return {
            'overall_quality': overall_quality,
            'quality_level': 'good' if overall_quality > 0.7 else 'fair' if overall_quality > 0.4 else 'poor',
            'metrics': quality_metrics,
            'recommendations': self._get_quality_recommendations(overall_quality)
        }

    def _get_quality_recommendations(self, quality_score: float) -> List[str]:
        """Get recommendations for improving transcript quality"""
        recommendations = []

        if quality_score < 0.5:
            recommendations.extend([
                "Speak more slowly and clearly",
                "Include specific details about your work",
                "Mention what you completed, are working on, or are blocked by"
            ])
        elif quality_score < 0.7:
            recommendations.extend([
                "Add more context to your update",
                "Be specific about tasks and progress"
            ])

        return recommendations

def process_voice_command(command: str) -> Dict[str, Any]:
    """Process voice commands for scrum actions"""
    command = command.lower().strip()

    # Define command patterns
    command_patterns = {
        'create_task': [
            r'create (?:a |an )?(?:new )?task(?: called| named)? (.+)',
            r'add (?:a |an )?(?:new )?task(?: called| named)? (.+)'
        ],
        'update_status': [
            r'(?:mark |update |change )(.+?)(?: as | to )(?:done|completed|finished|in progress|blocked)',
            r'(.+?)(?: is | has been )(?:done|completed|finished|in progress|blocked)'
        ],
        'show_board': [
            r'show (?:me |the )?(?:sprint |kanban )?board',
            r'open (?:the )?(?:sprint |kanban )?board'
        ],
        'add_blocker': [
            r'(?:i\'m |i am )?(?:blocked|stuck) (?:by |with |on )(.+)',
            r'(?:there\'s |there is )?(?:a |an )?blocker (.+)'
        ]
    }

    for command_type, patterns in command_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                return {
                    'command_type': command_type,
                    'extracted_data': match.groups(),
                    'confidence': 0.8
                }

    return {
        'command_type': 'unknown',
        'extracted_data': [],
        'confidence': 0.0
    }
