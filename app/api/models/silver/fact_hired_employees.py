"""
Hired Employees model module.

This module defines the HiredEmployee model for the database using SQLAlchemy ORM.
Follows dimensional modeling naming convention with 'fact_' prefix for fact tables.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import base
from datetime import datetime

class HiredEmployee(base):
    """
    HiredEmployee model class.
    
    Represents a fact table of hired employees in the organization.
    This is the main fact table that connects employees with their departments and jobs.
    
    Attributes:
        id_employee (int): The primary key of the employee
        name (str): The name of the employee (max 100 characters)
        datetime (DateTime): The date and time when the employee was hired (UTC)
        id_department (int): Foreign key to dim_departments table
        id_job (int): Foreign key to dim_jobs table
        department (Department): Relationship to department dimension
        job (Job): Relationship to job dimension
    
    Table name: fact_hired_employees
    Indexes:
        - id_employee (primary key)
        - id_department (foreign key)
        - id_job (foreign key)
        - datetime (for temporal queries)
    """
    __tablename__ = "fact_hired_employees"
    
    # Primary key
    id_employee = Column(Integer, primary_key=True, index=True)
    
    # Data fields
    name = Column(String(100), nullable=False)
    datetime = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Foreign keys
    id_department = Column(
        Integer, 
        ForeignKey("dim_departments.id_department", ondelete="RESTRICT"), 
        nullable=False,
        index=True
    )
    id_job = Column(
        Integer, 
        ForeignKey("dim_jobs.id_job", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    # Relationships
    department = relationship("Department", back_populates="employees")
    job = relationship("Job", back_populates="employees")
    
    def __repr__(self):
        """String representation of the HiredEmployee model."""
        return f"<{self.__tablename__}(id={self.id_employee}, name={self.name}, department_id={self.id_department}, job_id={self.id_job}, datetime={self.datetime})>" 