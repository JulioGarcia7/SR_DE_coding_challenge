"""
Job model module.

This module defines the Job model for the database using SQLAlchemy ORM.
Follows dimensional modeling naming convention with 'dim_' prefix.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import base

class Job(base):
    """
    Job model class.
    
    Represents a job dimension in the organization.
    
    Attributes:
        id_job (int): The primary key of the job
        job (str): The name or title of the job position (max 100 characters)
        employees (list): List of employees in this job position
    
    Table name: dim_jobs
    """
    __tablename__ = "dim_jobs"
    
    id_job = Column(Integer, primary_key=True)
    job = Column(String(100), nullable=False)
    
    # Relationships
    employees = relationship("HiredEmployee", back_populates="job")
    
    def __repr__(self):
        """String representation of the Job model."""
        return f"<{self.__tablename__}(id={self.id_job}, job={self.job})>" 