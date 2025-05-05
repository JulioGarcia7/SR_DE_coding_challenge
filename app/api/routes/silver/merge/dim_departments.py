"""
Department Silver Layer Routes

This module handles the transformation of department data
from bronze (staging) to silver (dimensional) layer.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.api.models import StgDepartments, DimDepartments

router = APIRouter()

@router.post("/merge", response_model=dict)
async def merge_departments(db: Session = Depends(get_db)):
    """
    Merge departments from staging to dimensional model.
    
    This endpoint:
    1. Transforms staging data to match dimensional model
    2. Performs upsert operation
    3. Returns merge statistics
    
    Returns:
        dict: Statistics about the merge operation
    """
    try:
        # Get initial count
        initial_count = db.execute(
            text("SELECT COUNT(*) FROM dim_departments")
        ).scalar()

        # Perform MERGE operation
        merge_query = """
        WITH staging_data AS (
            SELECT DISTINCT
                id::integer as id_department,
                department
            FROM stg_departments
            WHERE id IS NOT NULL
        )
        MERGE INTO dim_departments d
        USING staging_data s ON d.id_department = s.id_department
        WHEN MATCHED THEN
            UPDATE SET department = s.department
        WHEN NOT MATCHED THEN
            INSERT (id_department, department)
            VALUES (s.id_department, s.department);
        """
        
        db.execute(text(merge_query))
        
        # Get statistics
        stats_query = """
        SELECT 
            (SELECT COUNT(*) FROM dim_departments) as final_count,
            (SELECT COUNT(*) FROM stg_departments) as total_processed,
            (
                SELECT COUNT(*) 
                FROM dim_departments d
                WHERE EXISTS (
                    SELECT 1 FROM stg_departments s
                    WHERE s.id::integer = d.id_department
                )
            ) as matched_count
        """
        
        stats = db.execute(text(stats_query)).fetchone()
        
        db.commit()
        
        return {
            "message": "Departments merged successfully",
            "statistics": {
                "initial_count": initial_count,
                "final_count": stats.final_count,
                "total_processed": stats.total_processed,
                "inserted": stats.final_count - initial_count,
                "updated": stats.matched_count
            },
            "status": "success"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Error during merge operation",
                "error": str(e)
            }
        ) 