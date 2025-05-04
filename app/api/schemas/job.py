"""
Job schema module.

This module defines the Pydantic models for job data validation and serialization.
Currently only includes Bronze (staging) layer schemas.
"""

from pydantic import Field
from app.api.schemas.base import BaseSchema

class StgJobBase(BaseSchema):
    """Base schema for Staging Job with raw attributes from CSV."""
    id: str = Field(
        ...,
        description="Id of the job from CSV"
    )
    job: str = Field(
        ...,
        description="Name of the job from CSV"
    )

# # Silver Layer (Dimensional) Schemas - Commented out for now
# class DimJobBase(BaseSchema):
#     """Base schema for Dimensional Job with common attributes."""
#     job_name: str = Field(
#         ...,
#         min_length=1,
#         max_length=100,
#         description="The name of the job position"
#     )

# class DimJobCreate(DimJobBase):
#     """Schema for creating a new dimensional job record."""
#     pass

# class DimJobRead(DimJobBase):
#     """Schema for reading dimensional job data."""
#     id_job: int = Field(
#         ...,
#         gt=0,
#         description="The unique identifier of the job"
#     ) 