"""
Silver Layer Routes

This package contains all routes for the silver layer operations,
including dimensional model management and data transformations.
"""

from fastapi import APIRouter
from app.api.routes.silver.dim_departments import router as departments_router
from app.api.routes.silver.dim_jobs import router as jobs_router
from app.api.routes.silver.fact_hired_employees import router as hired_employees_router

router = APIRouter()

router.include_router(
    departments_router,
    prefix="/departments",
    tags=["silver-departments"]
)

router.include_router(
    jobs_router,
    prefix="/jobs",
    tags=["silver-jobs"]
)

router.include_router(
    hired_employees_router,
    prefix="/hired_employees",
    tags=["silver-hired-employees"]
) 