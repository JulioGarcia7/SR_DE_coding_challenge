"""
Main application module for the Globant Data Migration API.

This module initializes the FastAPI application and sets up the core API functionality.
It includes the root endpoint and configuration for API documentation.

Routes:
    /: Root endpoint that returns a welcome message
    /docs: Swagger UI documentation (provided by FastAPI)
    /redoc: ReDoc documentation (provided by FastAPI)
"""

from fastapi import FastAPI
from app.core.config import settings

# Initialize FastAPI application
app = FastAPI(
    title=settings.project_name,
    description="API for handling employee data migration and analytics",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc"  # ReDoc endpoint
)

@app.get("/")
async def root():
    """
    Root endpoint for the API.
    
    Returns a welcome message to confirm the API is running.
    
    Returns:
        dict: A dictionary containing a welcome message
    
    Example:
        Response:
            {
                "message": "Welcome to Globant Data Migration API"
            }
    """
    return {"message": "Welcome to Globant Data Migration API"}
