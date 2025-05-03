"""
Hired Employee schema module.

This module defines the Pydantic models for hired employee data validation and serialization.
Includes both staging (Bronze) and fact (Silver) schemas.
"""

from datetime import datetime
from pydantic import Field, validator
from app.api.schemas.base import BaseSchema

# Bronze Layer (Staging) Schemas
class StgHiredEmployeeBase(BaseSchema):
    """Base schema for Staging Hired Employee with raw attributes from CSV."""
    id: int = Field(
        ...,
        description="Id of the employee from CSV"
    )
    name: str = Field(
        ...,
        description="Name and surname of the employee from CSV"
    )
    datetime: str = Field(
        ...,
        description="Hire datetime in ISO format from CSV"
    )
    department_id: int = Field(
        ...,
        description="Id of the department from CSV"
    )
    job_id: int = Field(
        ...,
        description="Id of the job from CSV"
    )

# Silver Layer (Fact) Schemas
class FactHiredEmployeeBase(BaseSchema):
    """Base schema for Fact Hired Employee with common attributes."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The name of the employee"
    )
    datetime: datetime = Field(
        ...,
        description="The date and time when the employee was hired (UTC)"
    )
    id_department: int = Field(
        ...,
        gt=0,
        description="The ID of the department the employee belongs to"
    )
    id_job: int = Field(
        ...,
        gt=0,
        description="The ID of the job position the employee holds"
    )

    @validator('datetime')
    def datetime_must_not_be_future(cls, v):
        """Validate that hiring datetime is not in the future."""
        if v > datetime.utcnow():
            raise ValueError('hiring datetime cannot be in the future')
        return v

class FactHiredEmployeeCreate(FactHiredEmployeeBase):
    """Schema for creating a new fact hired employee record."""
    pass

class FactHiredEmployeeRead(FactHiredEmployeeBase):
    """Schema for reading fact hired employee data."""
    id_employee: int = Field(
        ...,
        gt=0,
        description="The unique identifier of the employee"
    )

class FactHiredEmployeeBatchCreate(BaseSchema):
    """Schema for batch creation of fact hired employee records."""
    employees: list[FactHiredEmployeeCreate] = Field(
        ...,
        min_items=1,
        max_items=1000,  # Limit batch size for performance
        description="List of employees to create"
    ) 