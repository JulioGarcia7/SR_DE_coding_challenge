"""
Job schema module.

This module defines the Pydantic models for job data validation and serialization.
Includes both staging (Bronze) and dimensional (Silver) schemas.
"""

from pydantic import Field
from app.api.schemas.base import BaseSchema

# Bronze Layer (Staging) Schemas
class StgJobBase(BaseSchema):
    """Base schema for Staging Job with raw attributes from CSV."""
    id: int = Field(
        ...,
        description="Id of the job from CSV"
    )
    job: str = Field(
        ...,
        description="Name of the job from CSV"
    )

# Silver Layer (Dimensional) Schemas
class DimJobBase(BaseSchema):
    """Base schema for Dimensional Job with common attributes."""
    job: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The name or title of the job position"
    )

class DimJobCreate(DimJobBase):
    """Schema for creating a new dimensional job."""
    pass

class DimJobRead(DimJobBase):
    """Schema for reading dimensional job data."""
    id_job: int = Field(
        ...,
        gt=0,
        description="The unique identifier of the job"
    ) 