"""
Bronze layer routes package.

This package contains all the API routes for the bronze (staging) layer.
"""

from fastapi import APIRouter
from .upload.departments import router as departments_upload_router
from .upload.jobs import router as jobs_upload_router
from .upload.hired_employees import router as hired_employees_upload_router

router = APIRouter()
router.include_router(departments_upload_router)
router.include_router(jobs_upload_router)
router.include_router(hired_employees_upload_router) 