# AI Scrum Master Frontend

React frontend for the AI Scrum Master application.

## Features

- Dashboard with sprint metrics and team standup summaries
- Kanban-style sprint board with drag-and-drop functionality
- Product backlog management
- Analytics and reporting with charts
- Sprint retrospective tools
- Voice input support for hands-free operation
- AI-powered insights and recommendations

## Tech Stack

- React 18
- Plain CSS (no frameworks)
- Chart.js for data visualization
- Web Speech API for voice input

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create a `.env` file in the root directory and add your API keys:
   ```
   REACT_APP_API_BASE_URL=http://localhost:8000
   REACT_APP_VOICE_API_KEY=your_voice_api_key_here
   REACT_APP_CHART_API_KEY=your_chart_api_key_here
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Build

To build the app for production:

```bash
npm run build
```

## Components

- `App.js`: Main application component with routing
- `Dashboard.js`: Overview of sprint progress and team updates
- `SprintBoard.js`: Kanban board for managing sprint tasks
- `Backlog.js`: Product backlog with user stories
- `Analytics.js`: Charts and metrics for team performance
- `Retrospective.js`: Sprint retrospective tools
- `VoiceInput.js`: Voice input component for accessibility

## API Integration

The frontend communicates with the FastAPI backend through the `api.js` utility file. All API calls are centralized there for easy maintenance.

## Styling

All styles are written in plain CSS located in `src/styles/main.css`. The design follows a clean, modern aesthetic suitable for agile teams.
