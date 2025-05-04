"""
Dimensional Job Model Module

This module defines the Job dimension model using SQLAlchemy ORM.
Part of the silver layer in the medallion architecture.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import base

class DimJobs(base):
    """
    Job Dimension Model (Silver Layer)
    
    Represents the job position dimension in the organization's data warehouse.
    Contains cleaned and validated job position data.
    
    Attributes:
        id_job (int): Primary key and surrogate key for the job position
        job (str): Official title of the job position (max 100 characters)
        employees (list): One-to-many relationship with hired employees
    
    Relationships:
        - One job can have many employees (one-to-many with fact_hired_employees)
    
    Table name: dim_jobs
    """
    __tablename__ = "dim_jobs"
    
    # Dimensional attributes
    id_job = Column(Integer, primary_key=True)
    job = Column(String(100), nullable=False)
    
    # Relationships
    employees = relationship(
        "FactHiredEmployees", 
        backref="job",
        lazy="dynamic"  # Lazy loading for better performance
    )
    
    def __repr__(self):
        """Returns a string representation of the Job dimension."""
        return f"<{self.__tablename__}(id={self.id_job}, job={self.job})>" 