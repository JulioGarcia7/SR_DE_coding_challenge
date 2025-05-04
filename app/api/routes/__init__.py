"""
API routes package.

This package contains all the API routes for the application.
Currently only includes Bronze (staging) layer routes.
"""

from fastapi import APIRouter
from .bronze import router as bronze_router
# from .silver import router as silver_router

router = APIRouter()
router.include_router(bronze_router)
# router.include_router(silver_router)
