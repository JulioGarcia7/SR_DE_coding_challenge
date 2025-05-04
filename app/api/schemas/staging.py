"""
Staging schemas module.

This module defines the Pydantic models for staging data validation.
Only validates field names and stores everything as strings for the bronze layer.
"""

from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class StgDepartmentBase(BaseModel):
    """Base schema for staging department data."""
    id: str
    department: str

    model_config = ConfigDict(from_attributes=True)

class StgDepartmentCreate(StgDepartmentBase):
    """Schema for creating staging department data."""
    pass

class StgDepartment(StgDepartmentBase):
    """Schema for reading staging department data."""
    pass

class StgJobBase(BaseModel):
    """Base schema for staging job data."""
    id: str
    job: str

    model_config = ConfigDict(from_attributes=True)

class StgJobCreate(StgJobBase):
    """Schema for creating staging job data."""
    pass

class StgJob(StgJobBase):
    """Schema for reading staging job data."""
    pass

class StgHiredEmployeeBase(BaseModel):
    """Base schema for staging hired employee data."""
    id: str
    name: Optional[str] = None
    datetime: Optional[str] = None
    department_id: Optional[str] = None
    job_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class StgHiredEmployeeCreate(StgHiredEmployeeBase):
    """Schema for creating staging hired employee data."""
    pass

class StgHiredEmployee(StgHiredEmployeeBase):
    """Schema for reading staging hired employee data."""
    pass

class BatchUploadResponse(BaseModel):
    """Schema for batch upload response."""
    message: str
    rows_processed: int
    success: bool
    progress: List[str]

    model_config = ConfigDict(from_attributes=True) 