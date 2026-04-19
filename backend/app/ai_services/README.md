# AI Services

Internal AI services for the AI Scrum Master application using rule-based algorithms instead of external APIs.

## Overview

This module provides AI-powered features for scrum management without relying on external AI services. All processing is done using rule-based algorithms, pattern matching, and lexical analysis.

## Services

### 1. Summarization (`summarization.py`)
- **Purpose**: Summarize sprint data and meeting notes
- **Method**: Rule-based text analysis and keyword extraction
- **Features**:
  - Standup summary generation
  - Sprint progress summarization
  - Meeting notes analysis
  - Key insights extraction

### 2. Blocker Detection (`blocker_detection.py`)
- **Purpose**: Identify and categorize blockers from team updates
- **Method**: Pattern matching and keyword analysis
- **Features**:
  - Automatic blocker detection
  - Severity assessment
  - Category classification (technical, dependency, resource, etc.)
  - Solution hints generation
  - Impact analysis

### 3. Sentiment Analysis (`sentiment.py`)
- **Purpose**: Analyze sentiment in retrospective feedback
- **Method**: Lexical analysis with sentiment lexicons
- **Features**:
  - Feedback sentiment classification
  - Team morale assessment
  - Category-specific analysis
  - Actionable insights and recommendations

### 4. Voice Input Processing (`voice_input.py`)
- **Purpose**: Process voice transcripts for scrum updates
- **Method**: Text analysis and pattern matching
- **Features**:
  - Transcript classification (completed, in progress, blocked, planned)
  - Task extraction
  - Blocker identification
  - Voice command processing
  - Quality validation

## Architecture

Each service is implemented as a standalone Python class with the following structure:

```python
class ServiceName:
    def __init__(self):
        # Initialize lexicons, patterns, etc.

    def process_method(self, input_data):
        # Process input using rule-based algorithms
        # Return structured output
```

## Benefits of Internal AI

- **No API Costs**: No external service fees or rate limits
- **Data Privacy**: All processing happens locally
- **Customizable**: Easy to modify rules and lexicons for specific needs
- **Reliable**: No dependency on external service availability
- **Fast**: Local processing with minimal latency

## Usage Examples

### Summarization
```python
from summarization import SprintSummarizer

summarizer = SprintSummarizer()
summary = summarizer.summarize_standup(team_updates)
```

### Blocker Detection
```python
from blocker_detection import BlockerDetector

detector = BlockerDetector()
blockers = detector.detect_blockers(team_updates)
```

### Sentiment Analysis
```python
from sentiment import SentimentAnalyzer

analyzer = SentimentAnalyzer()
analysis = analyzer.analyze_retrospective_feedback(feedback_items)
```

### Voice Processing
```python
from voice_input import VoiceProcessor

processor = VoiceProcessor()
result = processor.process_voice_transcript(transcript)
```

## Configuration

Services use predefined lexicons and patterns that can be customized by modifying the class attributes:

- `positive_words` / `negative_words`: Sentiment lexicons
- `blocker_keywords`: Blocker detection patterns
- `update_keywords`: Voice input classification

## Testing

Run tests with:
```bash
pytest tests/
```

## Future Enhancements

While current implementation uses rule-based approaches, the architecture allows for future enhancements:

- Integration with local ML models
- More sophisticated NLP techniques
- Domain-specific training data
- Performance optimizations

## Dependencies

See `requirements.txt` for Python dependencies. The services are designed to work with minimal dependencies to keep the application lightweight.
