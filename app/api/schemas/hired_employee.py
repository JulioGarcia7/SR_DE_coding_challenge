"""
Hired Employee schema module.

This module defines the Pydantic models for hired employee data validation and serialization.
Currently only includes staging (Bronze) schemas.
"""

from datetime import datetime
from typing import List
from pydantic import Field, field_validator, ConfigDict
from app.api.schemas.base import BaseSchema

# Bronze Layer (Staging) Schemas
class StgHiredEmployeesBase(BaseSchema):
    """Base schema for Staging Hired Employee with raw attributes from CSV."""
    id: str = Field(
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
    department_id: str = Field(
        ...,
        description="Id of the department from CSV"
    )
    job_id: str = Field(
        ...,
        description="Id of the job from CSV"
    )