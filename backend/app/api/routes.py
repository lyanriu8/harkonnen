"""
    Main Router For Harkonnen
"""
from fastapi import APIRouter
from pydantic import BaseModel
from app.api.endpoints.client import sub_router as client_sub_router
from app.api.endpoints.master import sub_router as master_sub_router

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

# Include Subrouters
api_router.include_router(client_sub_router, prefix = "/client")
api_router.include_router(master_sub_router, prefix = "/master")
