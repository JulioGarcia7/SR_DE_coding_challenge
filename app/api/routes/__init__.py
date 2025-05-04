"""
API Routes Package

This package contains all API routes organized by layer:
- Bronze: Raw data ingestion
- Silver: Dimensional model operations
"""

from fastapi import APIRouter
from app.api.routes.bronze import router as bronze_router
from app.api.routes.silver import router as silver_router

router = APIRouter()

router.include_router(bronze_router, prefix="/bronze")
router.include_router(silver_router, prefix="/silver")
