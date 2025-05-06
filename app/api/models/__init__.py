"""
Data warehouse models.

This package implements the medallion architecture pattern:

Bronze Layer (Staging):
    - Raw data landing zone (stg_*)
    - Minimal transformations
    - Original data types preserved
    - No relationships enforced

Silver Layer:
    - Dimensions (dim_*): Clean, deduplicated reference data
    - Facts (fact_*): Clean, validated business events
    - Proper data types and relationships
    - Business rules enforced
"""

# Bronze Layer (Staging Models)
from app.api.models.bronze.stg_departments import StgDepartments
from app.api.models.bronze.stg_jobs import StgJobs
from app.api.models.bronze.stg_hired_employees import StgHiredEmployees

# Silver Layer (Dimensional Models)
from app.api.models.silver.dim_departments import DimDepartments
from app.api.models.silver.dim_jobs import DimJobs
from app.api.models.silver.fact_hired_employees import FactHiredEmployees

__all__ = [
    # Bronze Layer - Staging Tables
    "StgDepartments",  # Raw department data
    "StgJobs",        # Raw job position data
    "StgHiredEmployees",  # Raw employee hiring events
    
    # Silver Layer - Dimensional Model
    "DimDepartments",  # Department dimension
    "DimJobs",        # Job position dimension
    "FactHiredEmployees"  # Employee hiring fact table
]
