"""
Bronze jobs upload module.

This module defines the bulk upload endpoint for jobs data.
"""

from typing import List, Dict
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
import csv
import io
from sqlalchemy import text

from app.core.database import get_db
from app.api.models.bronze.stg_jobs import StgJobs
from app.api.schemas.staging import StgJobsCreate

router = APIRouter(
    prefix="/upload/jobs",
    tags=["bronze-upload"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_jobs(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Upload jobs data from CSV file in batches.
    First truncates the existing data, then loads the new data.
    
    Args:
        file: CSV file with jobs data
        db: Database session
    
    Returns:
        Dict with summary of processed batches
    
    Raises:
        HTTPException: If file format is invalid or batch size exceeds limit
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are allowed"
        )
    
    try:
        # Get current count
        result = db.execute(text("SELECT COUNT(*) FROM stg_jobs")).scalar()
        rows_before = result if result is not None else 0
        
        # Truncate the table before loading new data
        db.execute(text("TRUNCATE TABLE stg_jobs"))
        db.commit()
        
        content = await file.read()
        csv_data = io.StringIO(content.decode())
        reader = csv.reader(csv_data)
        
        batch_size = 1000
        current_batch: List[dict] = []
        total_processed = 0
        total_batches = 0
        error_rows = []
        progress_messages = []
        
        for row_num, row in enumerate(reader, 1):
            try:
                if len(row) != 2:  # id, job
                    error_rows.append({
                        "row": row_num,
                        "data": row,
                        "error": "Invalid number of columns"
                    })
                    continue
                
                job_data = {
                    "id": str(row[0]),
                    "job": row[1]
                }
                
                current_batch.append(job_data)
                
                # Process batch when it reaches the size limit
                if len(current_batch) >= batch_size:
                    await process_job_batch(current_batch, db)
                    total_processed += len(current_batch)
                    total_batches += 1
                    progress_messages.append(f"Procesadas {total_processed} filas")
                    current_batch = []
            
            except ValueError as e:
                error_rows.append({
                    "row": row_num,
                    "data": row,
                    "error": str(e)
                })
        
        # Process remaining records
        if current_batch:
            await process_job_batch(current_batch, db)
            total_processed += len(current_batch)
            total_batches += 1
            progress_messages.append(f"Procesadas {total_processed} filas (lote final)")
        
        return {
            "message": f"Table stg_jobs truncated ({rows_before} rows removed) and file processed successfully",
            "total_processed": total_processed,
            "total_batches": total_batches,
            "progress": progress_messages,
            "errors": error_rows
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )

async def process_job_batch(
    batch_data: List[dict],
    db: Session
) -> None:
    """
    Process a batch of job records.
    
    Args:
        batch_data: List of job dictionaries
        db: Database session
    """
    try:
        for job_data in batch_data:
            # Check if job already exists
            existing = db.query(StgJobs).filter(
                StgJobs.id == job_data["id"]
            ).first()
            
            if existing:
                # Update existing record
                for key, value in job_data.items():
                    setattr(existing, key, value)
            else:
                # Create new record
                db_job = StgJobs(**job_data)
                db.add(db_job)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise e 