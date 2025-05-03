"""
Schemas package.

This module exports all schema models for easy importing.
"""

from app.api.schemas.base import BaseSchema, TimestampMixin
from app.api.schemas.department import (
    StgDepartmentBase,
    DimDepartmentBase, DimDepartmentCreate, DimDepartmentRead
)
from app.api.schemas.job import (
    StgJobBase,
    DimJobBase, DimJobCreate, DimJobRead
)
from app.api.schemas.hired_employee import (
    StgHiredEmployeeBase,
    FactHiredEmployeeBase, FactHiredEmployeeCreate, FactHiredEmployeeRead,
    FactHiredEmployeeBatchCreate
)

__all__ = [
    # Base schemas
    'BaseSchema',
    'TimestampMixin',
    
    # Bronze Layer (Staging) schemas
    'StgDepartmentBase',
    'StgJobBase',
    'StgHiredEmployeeBase',
    
    # Silver Layer (Dimensional) schemas
    'DimDepartmentBase',
    'DimDepartmentCreate',
    'DimDepartmentRead',
    'DimJobBase',
    'DimJobCreate',
    'DimJobRead',
    'FactHiredEmployeeBase',
    'FactHiredEmployeeCreate',
    'FactHiredEmployeeRead',
    'FactHiredEmployeeBatchCreate',
]
