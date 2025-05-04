"""
Staging Departments routes module.

This module defines the API endpoints for staging departments data.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.models.bronze.stg_departments import StgDepartment
from app.api.schemas.staging import StgDepartmentCreate, StgDepartment as StgDepartmentSchema

router = APIRouter(
    prefix="/staging/departments",
    tags=["staging-departments"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=StgDepartmentSchema, status_code=status.HTTP_201_CREATED)
def create_department(
    department: StgDepartmentCreate,
    db: Session = Depends(get_db)
) -> StgDepartment:
    """
    Create a new department in staging.
    
    Args:
        department: Department data from CSV
        db: Database session
    
    Returns:
        Created department
    
    Raises:
        HTTPException: If department with same ID already exists
    """
    # Check if department already exists
    db_department = db.query(StgDepartment).filter(StgDepartment.id == department.id).first()
    if db_department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department with id {department.id} already exists"
        )
    
    # Create new department
    db_department = StgDepartment(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

@router.get("/", response_model=List[StgDepartmentSchema])
def read_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[StgDepartment]:
    """
    Get all departments from staging.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
    
    Returns:
        List of departments
    """
    return db.query(StgDepartment).offset(skip).limit(limit).all()

@router.get("/{department_id}", response_model=StgDepartmentSchema)
def read_department(
    department_id: int,
    db: Session = Depends(get_db)
) -> StgDepartment:
    """
    Get a specific department from staging by ID.
    
    Args:
        department_id: ID of the department to get
        db: Database session
    
    Returns:
        Department data
    
    Raises:
        HTTPException: If department not found
    """
    department = db.query(StgDepartment).filter(StgDepartment.id == department_id).first()
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {department_id} not found"
        )
    return department

@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a department from staging.
    
    Args:
        department_id: ID of the department to delete
        db: Database session
    
    Raises:
        HTTPException: If department not found
    """
    department = db.query(StgDepartment).filter(StgDepartment.id == department_id).first()
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {department_id} not found"
        )
    db.delete(department)
    db.commit() 