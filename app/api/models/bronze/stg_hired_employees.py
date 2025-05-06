"""
Staging hired employees table (bronze layer).

This module defines the staging table for raw hired employee data from CSV.
All fields except id are stored as strings in the bronze layer and are nullable.
"""

from sqlalchemy import Column, String
from app.core.database import base

class StgHiredEmployees(base):
    """
    Staging hired employees table.
    
    Raw data landing table for hired employees from CSV.
    All fields except id are stored as strings and are nullable.
    
    Attributes:
        id (str): Id of the employee from CSV (Primary Key)
        name (str): Name of the employee from CSV (nullable)
        datetime (str): Hire datetime as string from CSV (nullable)
        department_id (str): Department id reference from CSV (nullable)
        job_id (str): Job id reference from CSV (nullable)
    
    Table name: stg_hired_employees
    """
    __tablename__ = "stg_hired_employees"
    
    # Source fields
    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    datetime = Column(String, nullable=True)
    department_id = Column(String, nullable=True)
    job_id = Column(String, nullable=True)
    
    def __repr__(self):
        """Staging hired employee record repr."""
        return f"<{self.__tablename__}(id={self.id}, name={self.name})>" 