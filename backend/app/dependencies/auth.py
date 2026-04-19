from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer()

# Simple API key authentication for demo purposes
# In production, use proper JWT or OAuth
API_KEY = os.getenv("API_KEY", "demo-api-key")

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API key from Authorization header"""
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# For demo purposes, we'll skip authentication on most endpoints
# In production, add Depends(verify_api_key) to protected routes
