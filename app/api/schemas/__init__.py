"""
Schemas package.

This module exports all schema models for easy importing.
Currently only includes Bronze (staging) layer schemas.
"""

from app.api.schemas.base import BaseSchema, TimestampMixin
from app.api.schemas.department import (
    StgDepartmentsBase,
    # DimDepartmentBase, DimDepartmentCreate, DimDepartmentRead
)
from app.api.schemas.job import (
    StgJobsBase,
    # DimJobBase, DimJobCreate, DimJobRead
)
from app.api.schemas.hired_employee import (
    StgHiredEmployeesBase,
    # FactHiredEmployeeBase, FactHiredEmployeeCreate, FactHiredEmployeeRead,
    # FactHiredEmployeeBatchCreate
)

__all__ = [
    # Base schemas
    'BaseSchema',
    'TimestampMixin',
    
    # Bronze Layer (Staging) schemas
    'StgDepartmentsBase',
    'StgJobsBase',
    'StgHiredEmployeesBase',
    
    # # Silver Layer (Dimensional) schemas - Commented out for now
    # 'DimDepartmentBase',
    # 'DimDepartmentCreate',
    # 'DimDepartmentRead',
    # 'DimJobBase',
    # 'DimJobCreate',
    # 'DimJobRead',
    # 'FactHiredEmployeeBase',
    # 'FactHiredEmployeeCreate',
    # 'FactHiredEmployeeRead',
    # 'FactHiredEmployeeBatchCreate',
]
