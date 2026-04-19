"""
Internal AI service for detecting blockers in team updates.
Uses pattern matching and rule-based analysis instead of external APIs.
"""

import re
from typing import List, Dict, Any, Tuple

class BlockerDetector:
    def __init__(self):
        # Blocker keywords and patterns
        self.blocker_keywords = [
            'blocked', 'blocking', 'stuck', 'issue', 'problem', 'cannot', 'unable',
            'waiting', 'depends', 'need', 'required', 'missing', 'broken', 'failed',
            'error', 'bug', 'crash', 'timeout', 'limit', 'restriction'
        ]

        self.severity_indicators = {
            'high': ['critical', 'urgent', 'emergency', 'showstopper', 'deadline', 'cannot proceed'],
            'medium': ['important', 'significant', 'major', 'blocking progress'],
            'low': ['minor', 'small', 'slight', 'inconvenient']
        }

        self.context_patterns = [
            r'cannot (?:continue|proceed|move forward)',
            r'waiting (?:for|on)',
            r'depends on',
            r'blocked by',
            r'stuck (?:on|with|at)',
            r'need .*? to',
            r'missing .*?(?:dependency|requirement|access|permission)'
        ]

    def detect_blockers(self, updates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect blockers from team updates"""
        blockers = []

        for update in updates:
            text = update.get('update', '').lower()
            person = update.get('person', 'Unknown')

            detected_blockers = self._analyze_text(text, person)
            blockers.extend(detected_blockers)

        return blockers

    def _analyze_text(self, text: str, person: str) -> List[Dict[str, Any]]:
        """Analyze text for blocker patterns"""
        blockers = []

        # Check for context patterns
        for pattern in self.context_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                blocker = self._extract_blocker_info(text, match, person)
                if blocker:
                    blockers.append(blocker)

        # Check for keyword-based blockers if no pattern matches
        if not blockers:
            keyword_matches = [kw for kw in self.blocker_keywords if kw in text]
            if keyword_matches:
                blocker = self._create_blocker(text, person, keyword_matches)
                if blocker:
                    blockers.append(blocker)

        return blockers

    def _extract_blocker_info(self, text: str, match: re.Match, person: str) -> Dict[str, Any]:
        """Extract detailed blocker information from matched pattern"""
        match_start = match.start()
        match_end = match.end()

        # Get context around the match (up to 100 chars before and after)
        context_start = max(0, match_start - 100)
        context_end = min(len(text), match_end + 100)
        context = text[context_start:context_end]

        # Determine severity
        severity = self._determine_severity(text)

        # Extract potential solution hints
        solution_hints = self._find_solution_hints(text)

        return {
            'person': person,
            'description': context.strip(),
            'severity': severity,
            'category': self._categorize_blocker(text),
            'solution_hints': solution_hints,
            'detected_at': 'pattern_matching',
            'confidence': 0.8  # Rule-based confidence
        }

    def _create_blocker(self, text: str, person: str, keywords: List[str]) -> Dict[str, Any]:
        """Create blocker from keyword matches"""
        severity = self._determine_severity(text)
        category = self._categorize_blocker(text)
        solution_hints = self._find_solution_hints(text)

        return {
            'person': person,
            'description': text[:200] + "..." if len(text) > 200 else text,
            'severity': severity,
            'category': category,
            'solution_hints': solution_hints,
            'detected_at': 'keyword_matching',
            'confidence': 0.6  # Lower confidence for keyword-only detection
        }

    def _determine_severity(self, text: str) -> str:
        """Determine blocker severity based on text analysis"""
        text_lower = text.lower()

        for severity, indicators in self.severity_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                return severity

        # Default to medium if no specific indicators
        return 'medium'

    def _categorize_blocker(self, text: str) -> str:
        """Categorize the type of blocker"""
        text_lower = text.lower()

        categories = {
            'technical': ['api', 'server', 'database', 'code', 'deployment', 'build', 'test'],
            'dependency': ['waiting', 'depends', 'need', 'missing', 'required'],
            'resource': ['access', 'permission', 'credential', 'environment', 'tool'],
            'communication': ['clarification', 'question', 'feedback', 'review'],
            'external': ['vendor', 'third-party', 'external', 'client', 'stakeholder']
        }

        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category

        return 'general'

    def _find_solution_hints(self, text: str) -> List[str]:
        """Find potential solution hints in the text"""
        hints = []
        text_lower = text.lower()

        # Look for mentions of potential solutions
        if 'need' in text_lower:
            hints.append("Check if required resources are available")
        if 'waiting' in text_lower:
            hints.append("Follow up with the person/resource being waited on")
        if 'access' in text_lower or 'permission' in text_lower:
            hints.append("Verify access permissions and credentials")
        if 'api' in text_lower:
            hints.append("Check API status and documentation")
        if 'environment' in text_lower:
            hints.append("Ensure correct environment configuration")

        return hints

    def prioritize_blockers(self, blockers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize blockers based on severity and impact"""
        priority_order = {'high': 3, 'medium': 2, 'low': 1}

        return sorted(
            blockers,
            key=lambda b: (
                priority_order.get(b.get('severity', 'low'), 1),
                b.get('confidence', 0)
            ),
            reverse=True
        )

def analyze_blocker_impact(blockers: List[Dict[str, Any]], team_size: int = 5) -> Dict[str, Any]:
    """Analyze the overall impact of blockers on the team"""
    if not blockers:
        return {'impact_level': 'none', 'description': 'No blockers detected'}

    high_severity = len([b for b in blockers if b.get('severity') == 'high'])
    total_blockers = len(blockers)

    if high_severity > 0:
        impact = 'high'
        description = f"{high_severity} high-severity blocker(s) affecting team progress"
    elif total_blockers / team_size > 0.5:
        impact = 'medium'
        description = f"Multiple blockers ({total_blockers}) impacting team velocity"
    else:
        impact = 'low'
        description = f"{total_blockers} minor blocker(s) identified"

    return {
        'impact_level': impact,
        'description': description,
        'total_blockers': total_blockers,
        'high_severity_count': high_severity
    }
