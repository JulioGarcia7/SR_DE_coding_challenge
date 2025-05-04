"""
Staging Jobs routes module.

This module defines the API endpoints for staging jobs data.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.models.bronze.stg_jobs import StgJob
from app.api.schemas.staging import StgJobCreate, StgJob as StgJobSchema

router = APIRouter(
    prefix="/staging/jobs",
    tags=["staging-jobs"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=StgJobSchema, status_code=status.HTTP_201_CREATED)
def create_job(
    job: StgJobCreate,
    db: Session = Depends(get_db)
) -> StgJob:
    """
    Create a new job in staging.
    
    Args:
        job: Job data from CSV
        db: Database session
    
    Returns:
        Created job
    
    Raises:
        HTTPException: If job with same ID already exists
    """
    # Check if job already exists
    db_job = db.query(StgJob).filter(StgJob.id == job.id).first()
    if db_job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job with id {job.id} already exists"
        )
    
    # Create new job
    db_job = StgJob(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/", response_model=List[StgJobSchema])
def read_jobs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[StgJob]:
    """
    Get all jobs from staging.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
    
    Returns:
        List of jobs
    """
    return db.query(StgJob).offset(skip).limit(limit).all()

@router.get("/{job_id}", response_model=StgJobSchema)
def read_job(
    job_id: int,
    db: Session = Depends(get_db)
) -> StgJob:
    """
    Get a specific job from staging by ID.
    
    Args:
        job_id: ID of the job to get
        db: Database session
    
    Returns:
        Job data
    
    Raises:
        HTTPException: If job not found
    """
    job = db.query(StgJob).filter(StgJob.id == job_id).first()
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id {job_id} not found"
        )
    return job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a job from staging.
    
    Args:
        job_id: ID of the job to delete
        db: Database session
    
    Raises:
        HTTPException: If job not found
    """
    job = db.query(StgJob).filter(StgJob.id == job_id).first()
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id {job_id} not found"
        )
    db.delete(job)
    db.commit() 