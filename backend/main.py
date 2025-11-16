"""
    Harkonnen Backend Entrypoint

"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.core.config import settings


app = FastAPI(
    title="Harkonnen Backend API",
    description="Backend API Harkonnen",
    version="0.1.0",
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5190",  # Your Vite dev server
        "http://localhost:5173",  # Alternative Vite port
        "http://127.0.0.1:5190",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)


# Root Endpooint
@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": settings.APP_NAME, 
        "version": settings.VERSION, 
        "status": "running",
        "environment": "development",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,  
        port=settings.PORT  
    )