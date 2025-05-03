"""
Department schema module.

This module defines the Pydantic models for department data validation and serialization.
Includes both staging (Bronze) and dimensional (Silver) schemas.
"""

from pydantic import Field
from app.api.schemas.base import BaseSchema

# Bronze Layer (Staging) Schemas
class StgDepartmentBase(BaseSchema):
    """Base schema for Staging Department with raw attributes from CSV."""
    id: int = Field(
        ...,
        description="Id of the department from CSV"
    )
    department: str = Field(
        ...,
        description="Name of the department from CSV"
    )

# Silver Layer (Dimensional) Schemas
class DimDepartmentBase(BaseSchema):
    """Base schema for Dimensional Department with common attributes."""
    department: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The name of the department"
    )

class DimDepartmentCreate(DimDepartmentBase):
    """Schema for creating a new dimensional department."""
    pass

class DimDepartmentRead(DimDepartmentBase):
    """Schema for reading dimensional department data."""
    id_department: int = Field(
        ...,
        gt=0,
        description="The unique identifier of the department"
    ) 