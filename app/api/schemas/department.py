"""
Department schema module.

This module defines the Pydantic models for department data validation and serialization.
Currently only includes Bronze (staging) layer schemas.
"""

from pydantic import Field
from app.api.schemas.base import BaseSchema

class StgDepartmentsBase(BaseSchema):
    """Base schema for Staging Department with raw attributes from CSV."""
    id: str = Field(
        ...,
        description="Id of the department from CSV"
    )
    department: str = Field(
        ...,
        description="Name of the department from CSV"
    )