"""
Bronze/Staging Hired Employees model module.

This module defines the staging table for raw hired employees data from CSV.
"""

from sqlalchemy import Column, Integer, String
from app.core.database import base

class StgHiredEmployee(base):
    """
    Staging Hired Employee model class (Bronze Layer).
    
    Raw data landing table for hired employees from CSV.
    
    Attributes:
        id (int): Id of the employee from CSV
        name (str): Name and surname of the employee from CSV
        datetime (str): Hire datetime in ISO format from CSV
        department_id (int): Id of the department from CSV
        job_id (int): Id of the job from CSV
    
    Table name: stg_hired_employees
    Note: No primary key as this is a staging table
    """
    __tablename__ = "stg_hired_employees"
    
    # Fields from CSV
    id = Column(Integer)
    name = Column(String)
    datetime = Column(String)  # Keep as string for exact CSV data
    department_id = Column(Integer)
    job_id = Column(Integer)
    
    def __repr__(self):
        """String representation of the Staging Hired Employee model."""
        return f"<{self.__tablename__}(id={self.id}, name={self.name}, datetime={self.datetime})>" 