from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.core.database import get_db
from app.api.schemas.gold.metrics import HiredByQuarterResponse, DepartmentAboveMeanResponse

router = APIRouter(
    prefix="/metrics",
    tags=["gold-metrics"]
)

@router.get("/hired_by_quarter", response_model=List[HiredByQuarterResponse])
def get_hired_by_quarter(db: Session = Depends(get_db)):
    try:
        query = text('''
            SELECT
                d.department AS department,
                j.job AS job,
                SUM(CASE WHEN EXTRACT(QUARTER FROM f.hire_datetime) = 1 THEN 1 ELSE 0 END) AS q1,
                SUM(CASE WHEN EXTRACT(QUARTER FROM f.hire_datetime) = 2 THEN 1 ELSE 0 END) AS q2,
                SUM(CASE WHEN EXTRACT(QUARTER FROM f.hire_datetime) = 3 THEN 1 ELSE 0 END) AS q3,
                SUM(CASE WHEN EXTRACT(QUARTER FROM f.hire_datetime) = 4 THEN 1 ELSE 0 END) AS q4
            FROM fact_hired_employees f
            JOIN dim_departments d ON f.id_department = d.id_department
            JOIN dim_jobs j ON f.id_job = j.id_job
            WHERE EXTRACT(YEAR FROM f.hire_datetime) = 2021
            GROUP BY d.department, j.job
            ORDER BY d.department ASC, j.job ASC;
        ''')
        result = db.execute(query)
        rows = result.fetchall()
        return [HiredByQuarterResponse(
            department=row[0], job=row[1], q1=row[2], q2=row[3], q3=row[4], q4=row[5]
        ) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/departments_above_mean", response_model=List[DepartmentAboveMeanResponse])
def get_departments_above_mean(db: Session = Depends(get_db)):
    try:
        query = text('''
            WITH hires_per_department AS (
                SELECT
                    d.id_department,
                    d.department,
                    COUNT(*) AS hired
                FROM fact_hired_employees f
                JOIN dim_departments d ON f.id_department = d.id_department
                WHERE EXTRACT(YEAR FROM f.hire_datetime) = 2021
                GROUP BY d.id_department, d.department
            ),
            mean_hired AS (
                SELECT AVG(hired) AS mean_hired FROM hires_per_department
            )
            SELECT
                h.id_department AS id,
                h.department,
                h.hired
            FROM hires_per_department h, mean_hired m
            WHERE h.hired > m.mean_hired
            ORDER BY h.hired DESC;
        ''')
        result = db.execute(query)
        rows = result.fetchall()
        return [DepartmentAboveMeanResponse(id=row[0], department=row[1], hired=row[2]) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 