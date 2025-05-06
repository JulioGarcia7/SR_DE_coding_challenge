"""
Hired employees fact table model.

This module defines the Fact table for hired employees using SQLAlchemy ORM.
Follows dimensional modeling naming convention with 'fact_' prefix.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from app.core.database import base

class FactHiredEmployees(base):
    """
    Hired employees fact table.
    
    Represents the fact table for hired employees in the organization.
    Contains metrics and references to dimension tables.
    
    Attributes:
        id_employee (int): The primary key of the employee
        name (str): Name of the employee (max 100 characters)
        hire_datetime (DateTime): Date and time when the employee was hired
        id_department (int): Foreign key to dim_departments (protected from deletion)
        id_job (int): Foreign key to dim_jobs (protected from deletion)
        created_timestamp (datetime): Timestamp when the record was created
        updated_timestamp (datetime): Timestamp when the record was last updated
    
    Foreign Key Behavior:
        - department_id: RESTRICT - Prevents deletion of departments with employees
        - job_id: RESTRICT - Prevents deletion of jobs with employees
    
    Table name: fact_hired_employees
    """
    __tablename__ = "fact_hired_employees"
    
    # Primary key
    id_employee = Column(Integer, primary_key=True)
    
    # Attributes
    name = Column(String(100), nullable=False)
    hire_datetime = Column(DateTime, nullable=False)
    
    # Foreign keys to dimensions with delete protection
    id_department = Column(
        Integer, 
        ForeignKey(
            "dim_departments.id_department", 
            ondelete="RESTRICT",  # Prevent deleting departments with employees
            name="fk_fact_hired_employees_department"
        ),
        nullable=False,
        index=True
    )
    id_job = Column(
        Integer, 
        ForeignKey(
            "dim_jobs.id_job", 
            ondelete="RESTRICT",  # Prevent deleting jobs with employees
            name="fk_fact_hired_employees_job"
        ),
        nullable=False,
        index=True
    )
    
    # Audit timestamps
    created_timestamp = Column(DateTime, nullable=False, server_default=func.now())
    updated_timestamp = Column(DateTime, nullable=True, onupdate=func.now())
    
    # Create indexes for common queries
    __table_args__ = (
        Index('ix_fact_hired_employees_hire_datetime', 'hire_datetime'),
    )
    
    def __repr__(self):
        """String representation of the Hired Employees fact table."""
        return f"<{self.__tablename__}(id={self.id_employee}, name={self.name}, department_id={self.id_department}, job_id={self.id_job})>" 