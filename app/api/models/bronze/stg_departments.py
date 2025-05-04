"""
Bronze/Staging Department model module.

This module defines the staging table for raw department data from CSV.
All fields except id are stored as strings in the bronze layer and are nullable.
"""

from sqlalchemy import Column, String
from app.core.database import base

class StgDepartment(base):
    """
    Staging Department model class (Bronze Layer).
    
    Raw data landing table for departments from CSV.
    All fields except id are stored as strings and are nullable.
    
    Attributes:
        id (str): Id of the department from CSV (Primary Key)
        department (str): Name of the department from CSV (nullable)
    
    Table name: stg_departments
    """
    __tablename__ = "stg_departments"
    
    # Fields from CSV
    id = Column(String, primary_key=True)
    department = Column(String, nullable=True)
    
    def __repr__(self):
        """String representation of the Staging Department model."""
        return f"<{self.__tablename__}(id={self.id}, department={self.department})>" 