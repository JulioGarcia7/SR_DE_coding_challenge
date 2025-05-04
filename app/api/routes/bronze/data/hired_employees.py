"""
Staging Hired Employees routes module.

This module defines the API endpoints for staging hired employees data.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.models.bronze.stg_hired_employees import StgHiredEmployee
from app.api.schemas.staging import StgHiredEmployeeCreate, StgHiredEmployee as StgHiredEmployeeSchema

router = APIRouter(
    prefix="/staging/hired_employees",
    tags=["staging-hired-employees"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=StgHiredEmployeeSchema, status_code=status.HTTP_201_CREATED)
def create_hired_employee(
    hired_employee: StgHiredEmployeeCreate,
    db: Session = Depends(get_db)
) -> StgHiredEmployee:
    """
    Create a new hired employee record in staging.
    
    Args:
        hired_employee: Hired employee data
        db: Database session
    
    Returns:
        Created hired employee record
    
    Raises:
        HTTPException: If employee with same ID already exists
    """
    # Check if employee already exists
    db_employee = db.query(StgHiredEmployee).filter(StgHiredEmployee.id == hired_employee.id).first()
    if db_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Hired employee with id {hired_employee.id} already exists"
        )
    
    # Create new hired employee record
    db_employee = StgHiredEmployee(**hired_employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/", response_model=List[StgHiredEmployeeSchema])
def read_hired_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[StgHiredEmployee]:
    """
    Get all hired employees from staging.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
    
    Returns:
        List of hired employees
    """
    return db.query(StgHiredEmployee).offset(skip).limit(limit).all()

@router.get("/{employee_id}", response_model=StgHiredEmployeeSchema)
def read_hired_employee(
    employee_id: int,
    db: Session = Depends(get_db)
) -> StgHiredEmployee:
    """
    Get a specific hired employee from staging by ID.
    
    Args:
        employee_id: ID of the hired employee to get
        db: Database session
    
    Returns:
        Hired employee data
    
    Raises:
        HTTPException: If hired employee not found
    """
    employee = db.query(StgHiredEmployee).filter(StgHiredEmployee.id == employee_id).first()
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hired employee with id {employee_id} not found"
        )
    return employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hired_employee(
    employee_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a hired employee from staging.
    
    Args:
        employee_id: ID of the hired employee to delete
        db: Database session
    
    Raises:
        HTTPException: If hired employee not found
    """
    employee = db.query(StgHiredEmployee).filter(StgHiredEmployee.id == employee_id).first()
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hired employee with id {employee_id} not found"
        )
    db.delete(employee)
    db.commit() 