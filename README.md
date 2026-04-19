# AI Scrum Master Backend

A FastAPI-based backend service for AI-powered Scrum Master functionality. Provides endpoints for processing standup inputs, voice transcripts, and generating insights including summaries, blocker detection, and action items.

## Features

- **Standup Input Processing**: Accept and process daily standup updates from team members
- **Voice Transcript Processing**: Handle voice inputs (already converted to text) with AI analysis
- **AI-Powered Insights**: Generate standup summaries, detect blockers, and extract action items
- **Health Check**: Service availability monitoring
- **Clean Architecture**: Service-layer architecture with Pydantic models
- **CORS Enabled**: Configured for React frontend integration
- **Environment Configuration**: .env based configuration management

## Project Structure

```
├── main.py                 # FastAPI application entry point
├── core/
│   └── config.py          # Configuration management
├── models/
│   ├── __init__.py
│   └── standup.py         # Pydantic models for standup data
├── services/
│   ├── __init__.py
│   └── standup_service.py # Business logic for standup processing
├── routers/
│   ├── __init__.py
│   ├── standup.py         # Standup-related API endpoints
│   └── insights.py        # Insights and analytics endpoints
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## API Endpoints

### Standup Endpoints (`/api/standup`)

- `POST /api/standup/input` - Submit standup input for processing
- `POST /api/standup/voice` - Submit voice transcript for processing
- `POST /api/standup/insights` - Generate insights from standup data
- `GET /api/standup/summary` - Get sample summary structure
- `GET /api/standup/blockers` - Get sample blockers structure
- `GET /api/standup/action-items` - Get sample action items structure

### Insights Endpoints (`/api/insights`)

- `GET /api/insights/summary` - Get insights summary
- `GET /api/insights/blockers/recent` - Get recent blockers
- `GET /api/insights/action-items/pending` - Get pending action items
- `POST /api/insights/analytics/generate` - Generate team analytics

### Health Check

- `GET /health` - Service health check
- `GET /` - API root information

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file (optional):
```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
CORS_ORIGINS=http://localhost:3000
```

3. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

## Usage Examples

### Submit Standup Input

```python
import requests

data = {
    "updates": [
        {
            "person": "Alice",
            "update": "Completed user authentication feature. Will work on dashboard tomorrow."
        },
        {
            "person": "Bob",
            "update": "Blocked by API rate limiting issue. Need help from backend team."
        }
    ],
    "sprint_id": 1
}

response = requests.post("http://localhost:8000/api/standup/input", json=data)
insights = response.json()
```

### Submit Voice Transcript

```python
data = {
    "transcript": "I completed the login feature and will start working on the dashboard next",
    "person": "Alice",
    "confidence": 0.95
}

response = requests.post("http://localhost:8000/api/standup/voice", json=data)
result = response.json()
```

## Data Models

### StandupInput
- `updates`: List of team member updates
- `sprint_id`: Optional sprint identifier
- `team_id`: Optional team identifier

### VoiceTranscript
- `transcript`: The transcribed text
- `person`: Optional person identifier
- `confidence`: Optional transcription confidence

### StandupInsights (Response)
- `summary`: Standup summary with key metrics
- `blockers`: Detected blockers
- `action_items`: Extracted action items
- `recommendations`: AI-generated recommendations

## Architecture

The backend follows a clean service-layer architecture:

- **Routers**: Handle HTTP requests and responses
- **Services**: Contain business logic and orchestrate AI processing
- **Models**: Define data structures with Pydantic validation
- **Core**: Configuration and shared utilities

AI processing is handled by rule-based algorithms in the `ai_services` directory (imported at runtime), providing insights without external API dependencies.

## Development

- Uses FastAPI for high-performance async API development
- Pydantic for data validation and serialization
- Environment-based configuration
- CORS middleware for frontend integration
- Comprehensive API documentation with OpenAPI/Swagger

## Health Check

The `/health` endpoint returns:
```json
{
  "status": "healthy",
  "service": "AI Scrum Master API",
  "version": "1.0.0"
}
