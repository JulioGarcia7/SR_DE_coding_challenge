"""
Staging job table (bronze layer).

This module defines the staging table for raw job data from CSV.
All fields except id are stored as strings in the bronze layer and are nullable.
"""

from sqlalchemy import Column, String
from app.core.database import base

class StgJobs(base):
    """
    Staging job table.
    
    Raw data landing table for jobs from CSV.
    All fields except id are stored as strings and are nullable.
    
    Attributes:
        id (str): Id of the job from CSV (Primary Key)
        job (str): Title of the job from CSV (nullable)
    
    Table name: stg_jobs
    """
    __tablename__ = "stg_jobs"
    
    # Source fields
    id = Column(String, primary_key=True)
    job = Column(String, nullable=True)
    
    def __repr__(self):
        """Staging job record repr."""
        return f"<{self.__tablename__}(id={self.id}, job={self.job})>" 