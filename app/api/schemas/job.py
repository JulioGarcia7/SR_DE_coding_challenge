"""
Job schema module.

This module defines the Pydantic models for job data validation and serialization.
Currently only includes Bronze (staging) layer schemas.
"""

from pydantic import Field
from app.api.schemas.base import BaseSchema

class StgJobsBase(BaseSchema):
    """Base schema for Staging Job with raw attributes from CSV."""
    id: str = Field(
        ...,
        description="Id of the job from CSV"
    )
    job: str = Field(
        ...,
        description="Name of the job from CSV"
    )