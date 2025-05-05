"""
Bronze hired employees upload module.

This module defines the bulk upload endpoint for hired employees data.
"""

from typing import List, Dict, Optional, Tuple
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
import csv
import io
from datetime import datetime
from sqlalchemy import text

from app.core.database import get_db
from app.api.models.bronze.stg_hired_employees import StgHiredEmployees

router = APIRouter(
    prefix="/upload/hired_employees_csv",
    tags=["bronze-upload"],
    responses={404: {"description": "Not found"}}
)

def validate_datetime(date_str: str) -> bool:
    """Validate datetime string format."""
    try:
        if not date_str:
            return False
        datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False

def validate_row(row: List[str], row_num: int) -> Tuple[Optional[Dict], Optional[Dict]]:
    """
    Validate a row of data.
    
    Args:
        row: List of values from CSV
        row_num: Row number for error reporting
    
    Returns:
        Tuple of (data_dict, error_dict)
    """
    if len(row) != 5:  # id, name, datetime, department_id, job_id
        return None, {
            "row": row_num,
            "data": row,
            "error": "Invalid number of columns"
        }
    
    try:
        # Convert all IDs to strings
        employee_data = {
            "id": str(row[0]),
            "name": row[1],
            "datetime": row[2],
            "department_id": str(row[3]) if row[3] else None,
            "job_id": str(row[4]) if row[4] else None
        }
        
        # Validate datetime format
        if not validate_datetime(employee_data["datetime"]):
            return None, {
                "row": row_num,
                "data": row,
                "error": "Invalid datetime format"
            }
        
        return employee_data, None
        
    except ValueError as e:
        return None, {
            "row": row_num,
            "data": row,
            "error": str(e)
        }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_hired_employees(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Upload hired employees data from CSV file in batches.
    First truncates the existing data, then loads the new data.
    
    Args:
        file: CSV file with hired employees data
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
        result = db.execute(text("SELECT COUNT(*) FROM stg_hired_employees")).scalar()
        rows_before = result if result is not None else 0
        
        # Truncate the table before loading new data
        db.execute(text("TRUNCATE TABLE stg_hired_employees"))
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
            data, error = validate_row(row, row_num)
            
            if error:
                error_rows.append(error)
                continue
            
            current_batch.append(data)
            
            # Process batch when it reaches the size limit
            if len(current_batch) >= batch_size:
                await process_employee_batch(current_batch, db)
                total_processed += len(current_batch)
                total_batches += 1
                progress_messages.append(f"Procesadas {total_processed} filas")
                current_batch = []
        
        # Process remaining records
        if current_batch:
            await process_employee_batch(current_batch, db)
            total_processed += len(current_batch)
            total_batches += 1
            progress_messages.append(f"Procesadas {total_processed} filas (lote final)")
        
        return {
            "message": f"Table stg_hired_employees truncated ({rows_before} rows removed) and file processed successfully",
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

async def process_employee_batch(
    batch_data: List[dict],
    db: Session
) -> None:
    """
    Process a batch of hired employee records.
    
    Args:
        batch_data: List of employee dictionaries
        db: Database session
    """
    try:
        for employee_data in batch_data:
            # Check if employee already exists
            existing = db.query(StgHiredEmployees).filter(
                StgHiredEmployees.id == employee_data["id"]
            ).first()
            
            if existing:
                # Update existing record
                for key, value in employee_data.items():
                    setattr(existing, key, value)
            else:
                # Create new record
                db_employee = StgHiredEmployees(**employee_data)
                db.add(db_employee)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise e 