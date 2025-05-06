"""
Job dimension model.

This module defines the Job dimension model using SQLAlchemy ORM.
Part of the silver layer in the medallion architecture.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import base

class DimJobs(base):
    """
    Job dimension.
    
    Represents the job position dimension in the organization's data warehouse.
    Contains cleaned and validated job position data.
    
    Attributes:
        id_job (int): Primary key and surrogate key for the job position
        job (str): Official title of the job position (max 100 characters)
        created_timestamp (datetime): Timestamp when the record was created
        updated_timestamp (datetime): Timestamp when the record was last updated
        employees (list): One-to-many relationship with hired employees
    
    Relationships:
        - One job can have many employees (one-to-many with fact_hired_employees)
    
    Table name: dim_jobs
    """
    __tablename__ = "dim_jobs"
    
    # Dimensional attributes
    id_job = Column(Integer, primary_key=True)
    job = Column(String(100), nullable=False)
    created_timestamp = Column(DateTime, nullable=False, server_default=func.now())
    updated_timestamp = Column(DateTime, nullable=True, onupdate=func.now())
    
    # Employees relationship
    employees = relationship(
        "FactHiredEmployees", 
        backref="job",
        lazy="dynamic"
    )
    
    def __repr__(self):
        """Job dimension repr."""
        return f"<{self.__tablename__}(id={self.id_job}, job={self.job})>" 