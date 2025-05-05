"""
Silver Layer Routes

This package contains all routes for the silver layer operations,
including dimensional model management and data transformations.
"""

from fastapi import APIRouter
from .merge.dim_departments import router as departments_router
from .merge.dim_jobs import router as jobs_router
from .merge.fact_hired_employees import router as hired_employees_router

router = APIRouter()

# Include the routers for the silver layer operations
router.include_router(
    departments_router,
    prefix="/merge/dim_departments",
    tags=["silver-layer"]
)

router.include_router(
    jobs_router,
    prefix="/merge/dim_jobs",
    tags=["silver-layer"]
)

router.include_router(
    hired_employees_router,
    prefix="/merge/fact_hired_employees",
    tags=["silver-layer"]
) 