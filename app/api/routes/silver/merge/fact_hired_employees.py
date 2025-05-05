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

        # Get data quality statistics
        validation_query = """
        SELECT 
            COUNT(*) as total_records,
            SUM(CASE WHEN department_id IS NULL OR job_id IS NULL OR id IS NULL OR datetime IS NULL THEN 1 ELSE 0 END) as null_references,
            SUM(CASE 
                WHEN department_id IS NOT NULL AND job_id IS NOT NULL 
                AND NOT EXISTS (
                    SELECT 1 FROM dim_departments d 
                    WHERE d.id_department = department_id::integer
                ) THEN 1 
                ELSE 0 
            END) as invalid_departments,
            SUM(CASE 
                WHEN department_id IS NOT NULL AND job_id IS NOT NULL 
                AND NOT EXISTS (
                    SELECT 1 FROM dim_jobs j 
                    WHERE j.id_job = job_id::integer
                ) THEN 1 
                ELSE 0 
            END) as invalid_jobs
        FROM stg_hired_employees;
        """
        
        validation_result = db.execute(text(validation_query)).fetchone()

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
        
        # Get final statistics
        stats_query = """
        WITH staging_stats AS (
            SELECT 
                COUNT(*) as total_records,
                SUM(CASE 
                    WHEN id IS NOT NULL 
                    AND department_id IS NOT NULL 
                    AND job_id IS NOT NULL
                    AND datetime IS NOT NULL
                    AND EXISTS (
                        SELECT 1 FROM dim_departments d 
                        WHERE d.id_department = department_id::integer
                    )
                    AND EXISTS (
                        SELECT 1 FROM dim_jobs j 
                        WHERE j.id_job = job_id::integer
                    )
                THEN 1 ELSE 0 END) as valid_records
            FROM stg_hired_employees
        )
        SELECT 
            (SELECT COUNT(*) FROM fact_hired_employees) as final_count,
            s.total_records as total_processed,
            s.valid_records as valid_records,
            (
                SELECT COUNT(*)
                FROM fact_hired_employees f
                WHERE EXISTS (
                    SELECT 1 FROM stg_hired_employees s
                    WHERE s.id::integer = f.id_employee
                )
            ) as updated_records
        FROM staging_stats s;
        """
        
        stats = db.execute(text(stats_query)).fetchone()
        
        db.commit()
        
        return {
            "message": "Hired employees merged successfully",
            "statistics": {
                "initial_count": initial_count,
                "final_count": stats.final_count,
                "total_processed": stats.total_processed,
                "valid_records": stats.valid_records,
                "invalid_records": stats.total_processed - stats.valid_records,
                "updated": stats.updated_records,
                "inserted": stats.valid_records - stats.updated_records,
                "validation_details": {
                    "null_references": validation_result.null_references,
                    "invalid_departments": validation_result.invalid_departments,
                    "invalid_jobs": validation_result.invalid_jobs
                }
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