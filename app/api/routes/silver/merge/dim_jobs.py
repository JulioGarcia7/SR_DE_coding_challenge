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
                id::integer AS id_job,
                job
            FROM stg_jobs
            WHERE id IS NOT NULL
        )
        MERGE INTO dim_jobs AS target
        USING staging_data AS source
        ON target.id_job = source.id_job
        WHEN MATCHED AND target.job IS DISTINCT FROM source.job THEN
            UPDATE SET 
                job = source.job,
                updated_timestamp = CURRENT_TIMESTAMP
        WHEN NOT MATCHED THEN
            INSERT (id_job, job, created_timestamp, updated_timestamp)
            VALUES (
                source.id_job, 
                source.job,
                CURRENT_TIMESTAMP,
                NULL
            );
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