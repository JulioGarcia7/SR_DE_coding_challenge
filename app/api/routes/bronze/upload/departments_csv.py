"""
Bronze departments upload module.

This module defines the bulk upload endpoint for departments data.
"""

from typing import List, Dict
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
import csv
import io
from sqlalchemy import text
from fastapi.responses import JSONResponse

from app.core.database import get_db
from app.api.models.bronze.stg_departments import StgDepartments
from app.api.schemas.staging import StgDepartmentsCreate, BatchUploadResponse

router = APIRouter(
    prefix="/upload/departments_csv",
    tags=["bronze-layer"],
    responses={
        201: {"description": "Created"},
        204: {"description": "No data found in file."},
        400: {"description": "Bad Request"},
        500: {"description": "Internal Server Error"}
    },
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BatchUploadResponse)
async def upload_departments(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload departments data from CSV file in batches.
    First truncates the existing data, then loads the new data.
    
    Args:
        file: CSV file with departments data
        db: Database session
    
    Returns:
        BatchUploadResponse with summary of processed batches
    
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
        result = db.execute(text("SELECT COUNT(*) FROM stg_departments")).scalar()
        rows_before = result if result is not None else 0
        
        # Truncate the table before loading new data
        db.execute(text("TRUNCATE TABLE stg_departments"))
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
        row_count = 0
        
        for row_num, row in enumerate(reader, 1):
            row_count += 1
            try:
                if len(row) != 2:  # id, department
                    error_rows.append({
                        "row": row_num,
                        "data": row,
                        "error": "Invalid number of columns"
                    })
                    continue
                
                department_data = {
                    "id": str(row[0]),
                    "department": row[1]
                }
                
                current_batch.append(department_data)
                
                # Process batch when it reaches the size limit
                if len(current_batch) >= batch_size:
                    await process_department_batch(current_batch, db)
                    total_processed += len(current_batch)
                    total_batches += 1
                    progress_messages.append(f"Processed {total_processed} rows")
                    current_batch = []
            
            except ValueError as e:
                error_rows.append({
                    "row": row_num,
                    "data": row,
                    "error": str(e)
                })
        
        # Process remaining records
        if current_batch:
            await process_department_batch(current_batch, db)
            total_processed += len(current_batch)
            total_batches += 1
            progress_messages.append(f"Processed {total_processed} rows (final batch)")
        
        # New logic for status codes
        if row_count == 0:
            # File is empty
            return JSONResponse(
                status_code=204,
                content={
                    "message": "No data found in file.",
                    "total_processed": 0,
                    "total_batches": 0,
                    "progress": [],
                    "errors": []
                }
            )
        if total_processed == 0 and error_rows:
            # All rows invalid
            return JSONResponse(
                status_code=400,
                content={
                    "message": "No valid data processed. All rows invalid.",
                    "errors": error_rows
                }
            )
        return BatchUploadResponse(
            message=f"Table stg_departments truncated ({rows_before} rows removed) and file processed successfully",
            total_processed=total_processed,
            total_batches=total_batches,
            progress=progress_messages,
            errors=error_rows
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )

async def process_department_batch(
    batch_data: List[dict],
    db: Session
) -> None:
    """
    Process a batch of department records.
    
    Args:
        batch_data: List of department dictionaries
        db: Database session
    """
    try:
        for dept_data in batch_data:
            # Check if department already exists
            existing = db.query(StgDepartments).filter(
                StgDepartments.id == dept_data["id"]
            ).first()
            
            if existing:
                # Update existing record
                for key, value in dept_data.items():
                    setattr(existing, key, value)
            else:
                # Create new record
                db_department = StgDepartments(**dept_data)
                db.add(db_department)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise e # Rollback in case of error