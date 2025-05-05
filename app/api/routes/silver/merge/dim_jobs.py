"""
Job Silver Layer Routes

This module handles the transformation of job data
from bronze (staging) to silver (dimensional) layer.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.api.models import StgJobs, DimJobs

router = APIRouter()

@router.post("/merge", response_model=dict)
async def merge_jobs(db: Session = Depends(get_db)):
    """
    Merge jobs from staging to dimensional model.
    
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
            text("SELECT COUNT(*) FROM dim_jobs")
        ).scalar()

        # Perform MERGE operation
        merge_query = """
        WITH staging_data AS (
            SELECT DISTINCT
                id::integer as id_job,
                job
            FROM stg_jobs
            WHERE id IS NOT NULL
        )
        MERGE INTO dim_jobs d
        USING staging_data s ON d.id_job = s.id_job
        WHEN MATCHED THEN
            UPDATE SET job = s.job
        WHEN NOT MATCHED THEN
            INSERT (id_job, job)
            VALUES (s.id_job, s.job);
        """
        
        db.execute(text(merge_query))
        
        # Get statistics
        stats_query = """
        SELECT 
            (SELECT COUNT(*) FROM dim_jobs) as final_count,
            (SELECT COUNT(*) FROM stg_jobs) as total_processed,
            (
                SELECT COUNT(*) 
                FROM dim_jobs d
                WHERE EXISTS (
                    SELECT 1 FROM stg_jobs s
                    WHERE s.id::integer = d.id_job
                )
            ) as matched_count
        """
        
        stats = db.execute(text(stats_query)).fetchone()
        
        db.commit()
        
        return {
            "message": "Jobs merged successfully",
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