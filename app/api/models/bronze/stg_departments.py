"""
Bronze/Staging Department model module.

This module defines the staging table for raw department data from CSV.
"""

from sqlalchemy import Column, Integer, String
from app.core.database import base

class StgDepartment(base):
    """
    Staging Department model class (Bronze Layer).
    
    Raw data landing table for departments from CSV.
    
    Attributes:
        id (int): Id of the department from CSV
        department (str): Name of the department from CSV
    
    Table name: stg_departments
    Note: No primary key as this is a staging table
    """
    __tablename__ = "stg_departments"
    
    # Fields from CSV
    id = Column(Integer)
    department = Column(String)
    
    def __repr__(self):
        """String representation of the Staging Department model."""
        return f"<{self.__tablename__}(id={self.id}, department={self.department})>" 