"""
Department model module.

This module defines the Department model for the database using SQLAlchemy ORM.
Follows dimensional modeling naming convention with 'dim_' prefix.
"""

from sqlalchemy import Column, Integer, String
from app.core.database import base

class DimDepartments(base):
    """
    Department model class.
    
    Represents a department dimension in the organization.
    
    Attributes:
        id_department (int): The primary key of the department
        department (str): The name of the department (max 100 characters)
    
    Table name: dim_departments
    """
    __tablename__ = "dim_departments"
    
    id_department = Column(Integer, primary_key=True)
    department = Column(String(100), nullable=False)
    
    def __repr__(self):
        """String representation of the Department model."""
        return f"<{self.__tablename__}(id={self.id_department}, department={self.department})>" 