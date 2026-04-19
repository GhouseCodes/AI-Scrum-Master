# AI Scrum Master

A comprehensive AI-powered Scrum Master web application for agile project management.

## Overview

This application provides teams with AI-assisted scrum management including:
- Sprint planning and tracking
- Kanban-style task boards
- Product backlog management
- Daily standup facilitation
- Sprint retrospectives
- Analytics and reporting
- Voice input support
- AI-powered insights and recommendations

## Architecture

The application is built with a clean separation of concerns:

- **Frontend**: React application with plain CSS
- **Backend**: FastAPI REST API
- **AI Services**: Internal rule-based AI (no external APIs)
- **Database**: SQLite (easily upgradeable to PostgreSQL/MySQL)

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. Clone the repository
2. Copy `.env.example` to `.env` and configure your settings
3. Run `docker-compose up --build`
4. Open http://localhost:3000 in your browser

### Local Development

1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **AI Services**: Already integrated into the backend

## Features

### Sprint Management
- Create and manage sprints
- Track sprint goals and progress
- Kanban board with drag-and-drop
- Sprint burndown charts

### Backlog Management
- Product backlog with user stories
- Story point estimation
- Priority management
- AI-powered backlog prioritization

### Daily Standups
- Team member updates
- AI analysis of standup notes
- Blocker detection and alerts
- Progress insights

### Analytics
- Velocity tracking
- Burndown charts
- Completion time analysis
- Team performance metrics

### AI Features
- **Summarization**: Automatic summarization of meetings and sprints
- **Blocker Detection**: Intelligent identification of impediments
- **Sentiment Analysis**: Analysis of retrospective feedback
- **Voice Input**: Voice command processing for hands-free operation

### Voice Support
- Voice input for updates
- Voice commands for actions
- Accessibility features

## API Documentation

The backend provides a REST API documented with OpenAPI/Swagger. When running locally, visit http://localhost:8000/docs for interactive API documentation.

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

- `API_KEY`: API authentication key
- `DATABASE_URL`: Database connection string
- `DEBUG`: Enable debug mode
- `REACT_APP_API_BASE_URL`: Frontend API endpoint

### AI Services

The AI services use internal rule-based algorithms and don't require external API keys. However, the architecture supports easy integration with external AI services if needed.

## Development

### Project Structure

```
ai-scrum-master/
├── frontend/          # React frontend
├── backend/           # FastAPI backend
├── ai-services/       # AI processing modules
├── docker/            # Docker configuration
├── docs/              # Documentation
└── docker-compose.yml # Multi-service orchestration
```

### Adding New Features

1. **Frontend**: Add components in `frontend/src/components/`
2. **Backend**: Add routes in `backend/app/routers/`
3. **AI**: Add services in `ai-services/`
4. **Models**: Define Pydantic models in `backend/app/models/`

## Deployment

### Docker 

```bash
 docker-compose up -d
```

### Manual Deployment

1. Build frontend: `cd frontend && npm run build`
2. Deploy backend: Configure your server to run the FastAPI app
3. Serve frontend: Use nginx or similar to serve the built files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue on GitHub or contact the development team.
