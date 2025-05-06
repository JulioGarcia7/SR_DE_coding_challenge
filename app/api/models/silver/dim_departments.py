"""
Department model module.

This module defines the Department model for the database using SQLAlchemy ORM.
Follows dimensional modeling naming convention with 'dim_' prefix.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import base

class DimDepartments(base):
    """
    Department model class.
    
    Represents a department dimension in the organization.
    
    Attributes:
        id_department (int): The primary key of the department
        department (str): The name of the department (max 100 characters)
        created_timestamp (datetime): Timestamp when the record was created
        updated_timestamp (datetime): Timestamp when the record was last updated
        employees (list): List of employees in this department (relationship)
    
    Table name: dim_departments
    """
    __tablename__ = "dim_departments"
    
    id_department = Column(Integer, primary_key=True)
    department = Column(String(100), nullable=False)
    created_timestamp = Column(DateTime, nullable=False, server_default=func.now())
    updated_timestamp = Column(DateTime, nullable=True, onupdate=func.now())
    
    # Relationships
    employees = relationship("FactHiredEmployees", backref="department")
    
    def __repr__(self):
        """String representation of the Department model."""
        return f"<{self.__tablename__}(id={self.id_department}, department={self.department})>" 