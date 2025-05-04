"""
Silver Layer Routes

This package contains all routes for the silver layer operations,
including dimensional model management and data transformations.
"""

from fastapi import APIRouter
from app.api.routes.silver.departments import router as departments_router

router = APIRouter()

router.include_router(
    departments_router,
    prefix="/departments",
    tags=["silver-departments"]
) 