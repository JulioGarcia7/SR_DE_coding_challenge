"""
Staging schemas module.

This module defines the Pydantic models for staging data validation.
Only validates field names and stores everything as strings for the bronze layer.
"""

from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class StgDepartmentsBase(BaseModel):
    """Base schema for staging department data."""
    id: str
    department: str

    model_config = ConfigDict(from_attributes=True)

class StgDepartmentsCreate(StgDepartmentsBase):
    """Schema for creating staging department data."""
    pass

class StgJobsBase(BaseModel):
    """Base schema for staging job data."""
    id: str
    job: str

    model_config = ConfigDict(from_attributes=True)

class StgJobsCreate(StgJobsBase):
    """Schema for creating staging job data."""
    pass

class StgHiredEmployeesBase(BaseModel):
    """Base schema for staging hired employee data."""
    id: str
    name: str
    datetime: str
    department_id: str
    job_id: str

    model_config = ConfigDict(from_attributes=True)

class StgHiredEmployeesCreate(StgHiredEmployeesBase):
    """Schema for creating staging hired employee data."""
    pass

class BatchUploadResponse(BaseModel):
    """Schema for batch upload response."""
    message: str
    total_processed: int
    total_batches: int
    progress: List[str]
    errors: List[dict] = []

    model_config = ConfigDict(from_attributes=True) 