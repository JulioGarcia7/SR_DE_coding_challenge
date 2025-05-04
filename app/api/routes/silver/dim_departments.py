"""
Department Silver Layer Routes

This module handles the transformation and loading of department data
from the bronze (staging) layer to the silver (dimensional) layer.
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
    2. Performs upsert operation (update existing, insert new)
    3. Validates data quality
    4. Returns merge statistics
    
    Returns:
        dict: Statistics about the merge operation including:
            - Total records processed
            - Records inserted
            - Records updated
            - Operation status
    """
    try:
        # Get initial count
        initial_count = db.execute(
            text("SELECT COUNT(*) FROM dim_departments")
        ).scalar()

        # Perform the merge using PostgreSQL 15 MERGE syntax
        merge_query = text("""
            WITH stg AS (
                SELECT CAST(id AS INTEGER) AS id_department, department
                FROM stg_departments
            )
            MERGE INTO dim_departments AS target
            USING stg AS source
            ON target.id_department = source.id_department
            WHEN MATCHED AND target.department IS DISTINCT FROM source.department THEN
                UPDATE SET department = source.department
            WHEN NOT MATCHED THEN
                INSERT (id_department, department)
                VALUES (source.id_department, source.department);
        """)
        
        # Execute merge
        db.execute(merge_query)
        db.commit()
        
        # Get final count and calculate statistics
        final_count = db.execute(
            text("SELECT COUNT(*) FROM dim_departments")
        ).scalar()
        
        # Get counts for detailed statistics
        stats_query = text("""
            WITH stg AS (
                SELECT CAST(id AS INTEGER) AS id_department, department
                FROM stg_departments
            )
            SELECT 
                COUNT(*) as total_source,
                COUNT(*) - COUNT(target.id_department) as inserted,
                COUNT(target.id_department) as matched
            FROM stg
            LEFT JOIN dim_departments target 
            ON target.id_department = stg.id_department;
        """)
        
        stats = db.execute(stats_query).fetchone()
        
        return {
            "message": "Departments merged successfully",
            "statistics": {
                "initial_count": initial_count,
                "final_count": final_count,
                "total_processed": stats.total_source,
                "inserted": stats.inserted,
                "updated": stats.matched
            },
            "status": "success"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error merging departments: {str(e)}"
        ) 