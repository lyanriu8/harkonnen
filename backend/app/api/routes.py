"""
    Main Router For Harkonnen
"""
from fastapi import APIRouter
from pydantic import BaseModel

# Create main API router
api_router = APIRouter()

class MessageResponse(BaseModel):
    """Simple message response model."""
    message: str
    status: str

@api_router.get("/health", response_model=MessageResponse)
def health_check():
    """Health check endpoint example."""
    return MessageResponse(message="Backend is running", status="healthy")
