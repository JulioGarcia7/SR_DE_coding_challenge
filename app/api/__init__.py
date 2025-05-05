"""
API package for data ingestion and transformation.
"""

from app.api.routes import router
from app.api.models import (
    StgDepartments, StgJobs, StgHiredEmployees,
    DimDepartments, DimJobs, FactHiredEmployees
) 