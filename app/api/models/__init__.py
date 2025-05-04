"""
Models package initialization.

This module exports all models following the medallion architecture:
- Bronze Layer: Raw/staging data (bronze_*)
# - Silver Layer: Validated dimensional models (dim_*, fact_*) - Commented out for now
"""

# Bronze Layer (Staging)
from app.api.models.bronze.stg_departments import StgDepartments
from app.api.models.bronze.stg_jobs import StgJobs
from app.api.models.bronze.stg_hired_employees import StgHiredEmployees

# # Silver Layer (Dimensions and Facts) - Commented out for now
# from app.api.models.silver.dim_departments import Department
# from app.api.models.silver.dim_jobs import Job
# from app.api.models.silver.fact_hired_employees import HiredEmployee

__all__ = [
    # Bronze Layer
    "StgDepartments",
    "StgJobs",
    "StgHiredEmployees",
    
    # # Silver Layer (Dimensions and Facts) - Commented out for now
    # "Department",  # from dim_departments
    # "Job",        # from dim_jobs
    # "HiredEmployee",  # from fact_hired_employees
]
