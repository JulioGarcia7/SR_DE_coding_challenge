"""
Staging department table (bronze layer).

This module defines the staging table for raw department data.
Part of the bronze layer in the medallion architecture.
Provides initial data landing with minimal transformations.
"""

from sqlalchemy import Column, String
from app.core.database import base

class StgDepartments(base):
    """
    Staging department table.
    
    Initial landing table for raw department data from source systems.
    Maintains original data types with minimal transformations.
    
    Attributes:
        id (str): Original department ID from source (Primary Key)
        department (str): Original department name from source (nullable)
    
    Data Handling:
        - All fields except ID are nullable to handle data quality issues
        - String types used to prevent data type conflicts on load
        - No relationships enforced at this layer
    
    Table name: stg_departments
    """
    __tablename__ = "stg_departments"
    
    # Source fields
    id = Column(String, primary_key=True)
    department = Column(String, nullable=True)
    
    def __repr__(self):
        """Staging department record repr."""
        return f"<{self.__tablename__}(id={self.id}, department={self.department})>" 