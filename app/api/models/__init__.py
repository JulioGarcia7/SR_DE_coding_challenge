"""
Models package initialization.

This module exports all models to make them easily importable from other parts of the application.
Example:
    from app.api.models import Department, Job, HiredEmployee
"""

from app.api.models.departments import Department
from app.api.models.jobs import Job
from app.api.models.hired_employees import HiredEmployee

__all__ = [
    "Department",
    "Job",
    "HiredEmployee"
]
