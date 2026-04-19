"""
Internal sentiment analysis service for retrospective feedback.
Uses rule-based lexical analysis instead of external APIs.
"""

import re
from typing import List, Dict, Any, Tuple
from collections import defaultdict

class SentimentAnalyzer:
    def __init__(self):
        # Sentiment lexicons
        self.positive_words = {
            'excellent', 'amazing', 'fantastic', 'great', 'good', 'wonderful', 'awesome',
            'brilliant', 'outstanding', 'superb', 'perfect', 'ideal', 'smooth', 'easy',
            'successful', 'productive', 'efficient', 'effective', 'helpful', 'supportive',
            'collaborative', 'transparent', 'clear', 'organized', 'structured', 'agile',
            'improved', 'better', 'progress', 'achievement', 'accomplished', 'delivered'
        }

        self.negative_words = {
            'terrible', 'awful', 'horrible', 'bad', 'worst', 'poor', 'disappointing',
            'frustrating', 'annoying', 'difficult', 'hard', 'challenging', 'problematic',
            'confusing', 'unclear', 'disorganized', 'chaotic', 'inefficient', 'wasteful',
            'blocked', 'stuck', 'failed', 'broken', 'buggy', 'delayed', 'overdue',
            'stressful', 'overwhelming', 'exhausting', 'demotivating', 'conflicted'
        }

        # Intensifiers and negations
        self.intensifiers = {'very', 'extremely', 'really', 'quite', 'so', 'too', 'highly'}
        self.negations = {'not', 'never', 'no', 'none', 'nothing', 'nobody', 'neither', 'nor'}

        # Context-specific sentiment for agile/scrum
        self.agile_context = {
            'positive': {
                'successful sprint', 'met goals', 'delivered on time', 'good velocity',
                'smooth process', 'effective standups', 'clear requirements', 'good communication',
                'helpful scrum master', 'productive retrospectives', 'continuous improvement'
            },
            'negative': {
                'failed sprint', 'missed goals', 'delayed delivery', 'low velocity',
                'bottleneck', 'unclear requirements', 'poor communication', 'unproductive meetings',
                'lack of direction', 'scope creep', 'technical debt'
            }
        }

    def analyze_retrospective_feedback(self, feedback_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze sentiment of retrospective feedback items"""
        analysis_results = []

        for item in feedback_items:
            text = item.get('text', '').lower()
            category = item.get('category', 'general')  # went_well, improve, action_items

            sentiment_score, confidence = self._calculate_sentiment(text)
            sentiment_label = self._score_to_label(sentiment_score)

            analysis_results.append({
                'id': item.get('id'),
                'category': category,
                'sentiment': sentiment_label,
                'score': sentiment_score,
                'confidence': confidence,
                'key_phrases': self._extract_sentiment_phrases(text),
                'intensity': self._calculate_intensity(text)
            })

        # Aggregate results
        return {
            'individual_analysis': analysis_results,
            'aggregate': self._aggregate_sentiment(analysis_results),
            'insights': self._generate_insights(analysis_results),
            'recommendations': self._generate_recommendations(analysis_results)
        }

    def _calculate_sentiment(self, text: str) -> Tuple[float, float]:
        """Calculate sentiment score and confidence"""
        words = re.findall(r'\b\w+\b', text)
        if not words:
            return 0.0, 0.0

        positive_score = 0
        negative_score = 0
        intensifier_count = 0
        negation_count = 0

        # Analyze each word
        for i, word in enumerate(words):
            if word in self.intensifiers:
                intensifier_count += 1
                continue
            if word in self.negations:
                negation_count += 1
                continue

            # Check for positive words
            if word in self.positive_words:
                score = 1
                # Apply intensifiers
                if i > 0 and words[i-1] in self.intensifiers:
                    score *= 1.5
                # Apply negations
                if i > 0 and words[i-1] in self.negations:
                    score *= -1
                positive_score += score

            # Check for negative words
            elif word in self.negative_words:
                score = -1
                # Apply intensifiers
                if i > 0 and words[i-1] in self.intensifiers:
                    score *= 1.5
                # Apply negations
                if i > 0 and words[i-1] in self.negations:
                    score *= -1
                negative_score += score

        # Check agile context phrases
        for phrase in self.agile_context['positive']:
            if phrase in text:
                positive_score += 2
        for phrase in self.agile_context['negative']:
            if phrase in text:
                negative_score -= 2

        # Calculate final score
        total_score = positive_score + negative_score
        max_possible = max(abs(positive_score), abs(negative_score), 1)
        normalized_score = total_score / max_possible

        # Calculate confidence based on evidence
        evidence_count = abs(positive_score) + abs(negative_score) + intensifier_count + negation_count
        confidence = min(evidence_count / len(words), 1.0)

        return normalized_score, confidence

    def _score_to_label(self, score: float) -> str:
        """Convert sentiment score to label"""
        if score > 0.3:
            return 'positive'
        elif score < -0.3:
            return 'negative'
        else:
            return 'neutral'

    def _extract_sentiment_phrases(self, text: str) -> List[str]:
        """Extract phrases that contribute to sentiment"""
        phrases = []
        words = re.findall(r'\b\w+\b', text)

        for i, word in enumerate(words):
            if word in self.positive_words or word in self.negative_words:
                # Get context around the word
                start = max(0, i-2)
                end = min(len(words), i+3)
                phrase = ' '.join(words[start:end])
                phrases.append(phrase)

        return phrases[:5]  # Return top 5 phrases

    def _calculate_intensity(self, text: str) -> str:
        """Calculate sentiment intensity"""
        intensifier_count = sum(1 for word in text.split() if word in self.intensifiers)
        exclamation_count = text.count('!')

        intensity_score = intensifier_count + exclamation_count

        if intensity_score >= 3:
            return 'high'
        elif intensity_score >= 1:
            return 'medium'
        else:
            return 'low'

    def _aggregate_sentiment(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate sentiment across all feedback items"""
        if not analysis_results:
            return {'overall_sentiment': 'neutral', 'distribution': {}}

        sentiment_counts = defaultdict(int)
        category_sentiment = defaultdict(lambda: defaultdict(int))

        total_score = 0
        total_confidence = 0

        for result in analysis_results:
            sentiment = result['sentiment']
            category = result['category']
            score = result['score']
            confidence = result['confidence']

            sentiment_counts[sentiment] += 1
            category_sentiment[category][sentiment] += 1
            total_score += score * confidence
            total_confidence += confidence

        # Calculate weighted average sentiment
        if total_confidence > 0:
            avg_score = total_score / total_confidence
            overall_sentiment = self._score_to_label(avg_score)
        else:
            overall_sentiment = 'neutral'

        return {
            'overall_sentiment': overall_sentiment,
            'distribution': dict(sentiment_counts),
            'category_breakdown': {cat: dict(counts) for cat, counts in category_sentiment.items()},
            'average_confidence': total_confidence / len(analysis_results) if analysis_results else 0
        }

    def _generate_insights(self, analysis_results: List[Dict[str, Any]]) -> List[str]:
        """Generate insights from sentiment analysis"""
        insights = []
        aggregate = self._aggregate_sentiment(analysis_results)

        overall = aggregate['overall_sentiment']
        distribution = aggregate['distribution']

        # Overall sentiment insight
        if overall == 'positive':
            insights.append("Team sentiment is generally positive - good morale and satisfaction levels")
        elif overall == 'negative':
            insights.append("Team sentiment shows concern - address negative feedback promptly")
        else:
            insights.append("Team sentiment is mixed - monitor for potential issues")

        # Distribution insights
        total_items = len(analysis_results)
        if total_items > 0:
            positive_pct = (distribution.get('positive', 0) / total_items) * 100
            negative_pct = (distribution.get('negative', 0) / total_items) * 100

            if positive_pct > 70:
                insights.append(".0f")
            elif negative_pct > 50:
                insights.append(".0f")

        # Category-specific insights
        category_breakdown = aggregate['category_breakdown']
        for category, sentiments in category_breakdown.items():
            category_total = sum(sentiments.values())
            if category_total > 0:
                neg_pct = (sentiments.get('negative', 0) / category_total) * 100
                if neg_pct > 60:
                    category_name = category.replace('_', ' ')
                    insights.append(".0f")

        return insights

    def _generate_recommendations(self, analysis_results: List[Dict[str, Any]]) -> List[str]:
        """Generate actionable recommendations based on sentiment"""
        recommendations = []
        aggregate = self._aggregate_sentiment(analysis_results)

        overall = aggregate['overall_sentiment']
        distribution = aggregate['distribution']

        if overall == 'negative':
            recommendations.extend([
                "Schedule follow-up meetings to address concerns",
                "Review process improvements based on feedback",
                "Consider team-building activities to boost morale"
            ])
        elif overall == 'positive':
            recommendations.extend([
                "Continue current successful practices",
                "Share positive experiences with other teams",
                "Document and replicate successful patterns"
            ])

        # Check for category-specific issues
        category_breakdown = aggregate['category_breakdown']
        for category, sentiments in category_breakdown.items():
            category_total = sum(sentiments.values())
            if category_total > 0:
                neg_pct = (sentiments.get('negative', 0) / category_total) * 100
                if neg_pct > 70:
                    if category == 'went_well':
                        recommendations.append("Investigate why positive aspects are being overshadowed")
                    elif category == 'could_improve':
                        recommendations.append("Prioritize improvements mentioned in feedback")
                    elif category == 'action_items':
                        recommendations.append("Review action items for feasibility and impact")

        return recommendations

def analyze_team_morale(feedback_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze overall team morale from retrospective feedback"""
    analyzer = SentimentAnalyzer()
    analysis = analyzer.analyze_retrospective_feedback(feedback_items)

    # Focus on morale indicators
    morale_score = 0
    morale_factors = []

    for item in analysis['individual_analysis']:
        if item['category'] == 'went_well' and item['sentiment'] == 'positive':
            morale_score += 1
            morale_factors.append('positive_experiences')
        elif item['category'] == 'could_improve' and item['sentiment'] == 'negative':
            morale_score -= 1
            morale_factors.append('process_concerns')

    # Normalize morale score
    max_possible = len(feedback_items)
    if max_possible > 0:
        normalized_morale = (morale_score + max_possible) / (2 * max_possible)
    else:
        normalized_morale = 0.5

    morale_level = 'high' if normalized_morale > 0.7 else 'medium' if normalized_morale > 0.4 else 'low'

    return {
        'morale_level': morale_level,
        'morale_score': normalized_morale,
        'key_factors': list(set(morale_factors)),
        'detailed_analysis': analysis
    }
