 # AI Scrum Master Backend

FastAPI backend for the AI Scrum Master application.

## Features

- REST API for sprint management
- User story backlog management
- Analytics and reporting
- AI-powered insights and recommendations
- Voice input processing
- CORS enabled for frontend integration

## Quick Start

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Open http://localhost:8000/docs for API documentation

### Docker

```bash
docker build -f docker/Dockerfile.backend -t scrum-backend .
docker run -p 8000:8000 scrum-backend
```

## API Endpoints

### Sprints
- `GET /sprints` - List all sprints
- `POST /sprints` - Create new sprint
- `GET /sprints/{id}` - Get sprint details
- `PUT /sprints/{id}` - Update sprint
- `DELETE /sprints/{id}` - Delete sprint

### Backlog
- `GET /backlog` - List user stories
- `POST /backlog` - Create user story
- `PUT /backlog/{id}` - Update user story
- `DELETE /backlog/{id}` - Delete user story

### Analytics
- `GET /analytics` - Get team analytics
- `GET /analytics/velocity` - Get velocity data
- `GET /analytics/burndown` - Get burndown chart data

### AI Services
- `POST /ai/insights` - Generate AI insights
- `POST /ai/sentiment` - Analyze sentiment
- `POST /ai/blockers` - Detect blockers
- `POST /ai/voice` - Process voice input
- `POST /ai/summarize` - Summarize content

## Configuration

Set environment variables in `.env`:

```env
API_KEY=your-api-key
DATABASE_URL=sqlite:///./scrum_master.db
DEBUG=True
SECRET_KEY=your-secret-key
```

## Development

### Project Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app
│   ├── config.py        # Configuration
│   ├── models/          # Pydantic models
│   ├── routers/         # API routes
│   ├── dependencies/    # Dependencies
│   └── ai_services.py   # AI service imports
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── README.md           # This file
```

### Adding New Endpoints

1. Create a new router in `app/routers/`
2. Add the router to `main.py`
3. Update the models if needed

### AI Integration

AI services are imported from the `ai-services` directory. Add new AI capabilities by:

1. Creating new modules in `ai-services/`
2. Importing them in `app/ai_services.py`
3. Adding API endpoints in `routers/ai.py`

## Testing

Run tests with:
```bash
pytest
```

## Deployment

The backend is containerized and can be deployed using Docker Compose with the main `docker-compose.yml` file.
