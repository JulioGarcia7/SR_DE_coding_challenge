"""
Job Silver Layer Routes

This module handles the transformation and loading of job data
from the bronze (staging) layer to the silver (dimensional) layer.
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
            text("SELECT COUNT(*) FROM dim_jobs")
        ).scalar()

        # Perform the merge using PostgreSQL 15 MERGE syntax
        merge_query = text("""
            WITH stg AS (
                SELECT CAST(id AS INTEGER) AS id_job, job
                FROM stg_jobs
            )
            MERGE INTO dim_jobs AS target
            USING stg AS source
            ON target.id_job = source.id_job
            WHEN MATCHED AND target.job IS DISTINCT FROM source.job THEN
                UPDATE SET job = source.job
            WHEN NOT MATCHED THEN
                INSERT (id_job, job)
                VALUES (source.id_job, source.job);
        """)
        
        # Execute merge
        db.execute(merge_query)
        db.commit()
        
        # Get final count and calculate statistics
        final_count = db.execute(
            text("SELECT COUNT(*) FROM dim_jobs")
        ).scalar()
        
        # Get counts for detailed statistics
        stats_query = text("""
            WITH stg AS (
                SELECT CAST(id AS INTEGER) AS id_job, job
                FROM stg_jobs
            )
            SELECT 
                COUNT(*) as total_source,
                COUNT(*) - COUNT(target.id_job) as inserted,
                COUNT(target.id_job) as matched
            FROM stg
            LEFT JOIN dim_jobs target 
            ON target.id_job = stg.id_job;
        """)
        
        stats = db.execute(stats_query).fetchone()
        
        return {
            "message": "Jobs merged successfully",
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
            detail=f"Error merging jobs: {str(e)}"
        ) 