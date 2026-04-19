"""
Configuration management using environment variables.
Provides centralized settings for the FastAPI application.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses pydantic for validation and type conversion.
    """

    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # CORS Configuration
    cors_origins: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

    # AI Service Configuration (for future external API integration)
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")

    # Database Configuration (for future database integration)
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./scrum_master.db")

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    api_key: Optional[str] = os.getenv("API_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
