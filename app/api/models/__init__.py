"""
Models package initialization.

This module exports all models following the medallion architecture:
- Bronze Layer: Raw/staging data (bronze_*)
- Silver Layer: Validated dimensional models (dim_*)
"""

# Bronze Layer (Staging)
from app.api.models.bronze.stg_departments import StgDepartments
from app.api.models.bronze.stg_jobs import StgJobs
from app.api.models.bronze.stg_hired_employees import StgHiredEmployees

# Silver Layer (Dimensions)
from app.api.models.silver.dim_departments import DimDepartments
from app.api.models.silver.dim_jobs import DimJobs

__all__ = [
    # Bronze Layer
    "StgDepartments",
    "StgJobs",
    "StgHiredEmployees",
    
    # Silver Layer (Dimensions)
    "DimDepartments",
    "DimJobs"
]
