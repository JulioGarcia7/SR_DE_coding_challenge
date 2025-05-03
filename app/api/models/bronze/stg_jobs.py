"""
Bronze/Staging Job model module.

This module defines the staging table for raw job data from CSV.
"""

from sqlalchemy import Column, Integer, String
from app.core.database import base

class StgJob(base):
    """
    Staging Job model class (Bronze Layer).
    
    Raw data landing table for jobs from CSV.
    
    Attributes:
        id (int): Id of the job from CSV
        job (str): Name of the job from CSV
    
    Table name: stg_jobs
    Note: No primary key as this is a staging table
    """
    __tablename__ = "stg_jobs"
    
    # Fields from CSV
    id = Column(Integer)
    job = Column(String)
    
    def __repr__(self):
        """String representation of the Staging Job model."""
        return f"<{self.__tablename__}(id={self.id}, job={self.job})>" 