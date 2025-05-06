"""
Fact Hired Employees Silver Layer Routes

This module handles the transformation of hired employees data
from bronze (staging) to silver (fact) layer, ensuring referential integrity.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.api.models import StgHiredEmployees, FactHiredEmployees

router = APIRouter()

@router.post("/merge", response_model=dict)
async def merge_hired_employees(db: Session = Depends(get_db)):
    """
    Merge hired employees from staging to fact table.
    
    This endpoint:
    1. Validates all foreign keys exist in dimension tables
    2. Transforms staging data to match fact table schema
    3. Performs upsert operation with strict referential integrity
    4. Returns detailed merge statistics
    
    Returns:
        dict: Statistics about the merge operation
    """
    try:
        # First, check if staging table has data
        staging_count = db.execute(
            text("SELECT COUNT(*) FROM stg_hired_employees")
        ).scalar()

        if staging_count == 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "No data found in staging table",
                    "hint": "Please load data into stg_hired_employees before attempting merge"
                }
            )

        # Get initial count
        initial_count = db.execute(
            text("SELECT COUNT(*) FROM fact_hired_employees")
        ).scalar() or 0

        # Perform MERGE operation only with valid records
        merge_query = """
        WITH valid_staging AS (
            SELECT 
                id::integer as id_employee,
                name,
                datetime::timestamp as hire_datetime,
                department_id::integer as id_department,
                job_id::integer as id_job
            FROM stg_hired_employees s
            WHERE 
                id IS NOT NULL 
                AND department_id IS NOT NULL 
                AND job_id IS NOT NULL
                AND datetime IS NOT NULL
                AND EXISTS (
                    SELECT 1 FROM dim_departments d 
                    WHERE d.id_department = s.department_id::integer
                )
                AND EXISTS (
                    SELECT 1 FROM dim_jobs j 
                    WHERE j.id_job = s.job_id::integer
                )
        )
        MERGE INTO fact_hired_employees f
        USING valid_staging s ON f.id_employee = s.id_employee
        WHEN MATCHED THEN
            UPDATE SET 
                name = s.name,
                hire_datetime = s.hire_datetime,
                id_department = s.id_department,
                id_job = s.id_job
        WHEN NOT MATCHED THEN
            INSERT (id_employee, name, hire_datetime, id_department, id_job)
            VALUES (
                s.id_employee, 
                s.name, 
                s.hire_datetime, 
                s.id_department, 
                s.id_job
            );
        """
        db.execute(text(merge_query))
        db.commit()

        # Get final statistics
        final_count = db.execute(
            text("SELECT COUNT(*) FROM fact_hired_employees")
        ).scalar() or 0

        valid_records = db.execute(
            text("""
                SELECT COUNT(*) FROM stg_hired_employees s
                WHERE 
                    id IS NOT NULL 
                    AND department_id IS NOT NULL 
                    AND job_id IS NOT NULL
                    AND datetime IS NOT NULL
                    AND EXISTS (
                        SELECT 1 FROM dim_departments d 
                        WHERE d.id_department = s.department_id::integer
                    )
                    AND EXISTS (
                        SELECT 1 FROM dim_jobs j 
                        WHERE j.id_job = s.job_id::integer
                    )
            """)
        ).scalar() or 0

        invalid_records = staging_count - valid_records

        return {
            "message": "Hired employees merged successfully",
            "statistics": {
                "initial_count": initial_count,
                "final_count": final_count,
                "total_processed": staging_count,
                "valid_records": valid_records,
                "invalid_records": invalid_records
            },
            "status": "success"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error during merge operation",
                "error": str(e),
                "hint": "Check validation details for specific issues"
            }
        ) 