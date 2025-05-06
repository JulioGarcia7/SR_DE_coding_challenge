"""
Bronze layer routes package.

This package contains all the API routes for the bronze (staging) layer.
"""

from fastapi import APIRouter
from .upload.departments_csv import router as departments_upload_router
from .upload.jobs_csv import router as jobs_upload_router
from .upload.hired_employees_csv import router as hired_employees_upload_router

router = APIRouter()

# Include the routers for the bronze layer operations
router.include_router(departments_upload_router)
router.include_router(jobs_upload_router)
router.include_router(hired_employees_upload_router) 