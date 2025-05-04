"""
Main application module for the Globant Data Migration API.

This module initializes the FastAPI application and sets up the core API functionality.
It includes the root endpoint and configuration for API documentation.

Routes:
    /: Root endpoint that returns a welcome message
    /docs: Swagger UI documentation (provided by FastAPI)
    /redoc: ReDoc documentation (provided by FastAPI)
    /api/v1/bronze/*: Bronze layer endpoints for data upload
"""

import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router as api_router

# Set recursion limit
sys.setrecursionlimit(3000)

# Initialize FastAPI application
app = FastAPI(
    title="Data Migration API",
    description="API for managing data migration between bronze, silver, and gold layers",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc"  # ReDoc endpoint
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

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
