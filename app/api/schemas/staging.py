"""
Staging schemas module.

This module defines the Pydantic models for staging data validation.
Only validates field names and stores everything as strings for the bronze layer.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict

class StgDepartmentBase(BaseModel):
    """Base schema for staging department data."""
    id: str
    department: str

    model_config = ConfigDict(from_attributes=True)

class StgDepartmentCreate(StgDepartmentBase):
    """Schema for creating a staging department record."""
    pass

class StgDepartment(StgDepartmentBase):
    """Schema for reading a staging department record."""
    pass

class StgJobBase(BaseModel):
    """Base schema for staging job data."""
    id: str
    job: str

    model_config = ConfigDict(from_attributes=True)

class StgJobCreate(StgJobBase):
    """Schema for creating a staging job record."""
    pass

class StgJob(StgJobBase):
    """Schema for reading a staging job record."""
    pass

class StgHiredEmployeeBase(BaseModel):
    """Base schema for staging hired employee data."""
    id: str
    name: str
    datetime: str
    department_id: str
    job_id: str

    model_config = ConfigDict(from_attributes=True)

class StgHiredEmployeeCreate(StgHiredEmployeeBase):
    """Schema for creating a staging hired employee record."""
    pass

class StgHiredEmployee(StgHiredEmployeeBase):
    """Schema for reading a staging hired employee record."""
    pass

class BatchUploadResponse(BaseModel):
    """Schema for batch upload response."""
    message: str
    rows_processed: int
    success: bool 