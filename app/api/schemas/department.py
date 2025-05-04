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

# # Silver Layer (Dimensional) Schemas - Commented out for now
# class DimDepartmentBase(BaseSchema):
#     """Base schema for Dimensional Department with common attributes."""
#     department_name: str = Field(
#         ...,
#         min_length=1,
#         max_length=100,
#         description="The name of the department"
#     )

# class DimDepartmentCreate(DimDepartmentBase):
#     """Schema for creating a new dimensional department record."""
#     pass

# class DimDepartmentRead(DimDepartmentBase):
#     """Schema for reading dimensional department data."""
#     id_department: int = Field(
#         ...,
#         gt=0,
#         description="The unique identifier of the department"
#     ) 