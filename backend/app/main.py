from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import sprints, backlog, analytics, ai, standup, insights
from .core.config import settings

app = FastAPI(
    title="AI Scrum Master API",
    description="Backend API for AI-powered Scrum Master application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sprints.router, prefix="/sprints", tags=["sprints"])
app.include_router(backlog.router, prefix="/backlog", tags=["backlog"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(standup.router, prefix="/api/standup", tags=["standup"])
app.include_router(insights.router, prefix="/api/insights", tags=["insights"])

@app.get("/")
async def root():
    return {"message": "AI Scrum Master API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
