# SR_DE_coding_challenge

## Project Overview
This project implements a data migration API following a **three-layer medallion architecture** (Bronze, Silver, Gold) for efficient data processing, analytics, and business reporting. The system processes employee hiring data through a robust ETL pipeline, transforming raw CSV data into a dimensional model and exposing business metrics via analytical endpoints.

## Architecture Flow Diagram
```
[Start] → [CSV Files]
    ↓
[Bronze Layer (Staging)]
    │
    ├─→ [stg_departments]
    │       - id (STRING)
    │       - department (STRING)
    │
    ├─→ [stg_jobs]
    │       - id (STRING)
    │       - job (STRING)
    │
    └─→ [stg_hired_employees]
            - id (STRING)
            - name (STRING)
            - datetime (STRING)
            - department_id (STRING)
            - job_id (STRING)
    ↓ [Transformation & Validation]
[Silver Layer (Dimensional Model)]
    │
    ├─→ [dim_departments]
    │       - id_department (INTEGER PK)
    │       - department (VARCHAR)
    │
    ├─→ [dim_jobs]
    │       - id_job (INTEGER PK)
    │       - job (VARCHAR)
    │
    └─→ [fact_hired_employees]
            - id_employee (INTEGER PK)
            - name (VARCHAR)
            - hire_datetime (TIMESTAMP)
            - id_department (INTEGER FK)
            - id_job (INTEGER FK)
    ↓ [Analytics & Reporting]
[Gold Layer (Analytics & Metrics)]
    │
    ├─→ [Gold Layer API]
    │       GET /api/v1/gold/metrics/hired_by_quarter
    │       GET /api/v1/gold/metrics/departments_above_mean
    │
    └─→ [Silver Layer API]
            POST /api/v1/silver/merge/dim_departments/merge
            POST /api/v1/silver/merge/dim_jobs/merge
            POST /api/v1/silver/merge/fact_hired_employees/merge
```

## Architecture Details

### Bronze Layer (Staging)
The Bronze layer serves as the initial landing zone for raw data:
- Accepts CSV file uploads through API endpoints
- Preserves source data in its original form (all fields as strings)
- Implements basic validation for file format and structure
- Provides batch processing capabilities for large datasets
- Tracks data quality metrics and upload statistics
- Tables are prefixed with 'stg_' for clear identification

### Silver Layer (Dimensional Model)
The Silver layer implements a star schema for analytical queries:
- Transforms and cleanses data from Bronze layer
- Enforces proper data types and constraints
- Implements business rules and data validation
- Maintains referential integrity
- Provides detailed merge statistics
- Uses 'dim_' prefix for dimensions and 'fact_' for fact tables

### Gold Layer (Analytics & Metrics)
The Gold layer provides analytical endpoints for business metrics and reporting, built on top of the cleaned and dimensional data from the Silver layer.
- Exposes business KPIs and aggregated reports via API endpoints
- Uses dimensional tables as source (no new tables required)
- Endpoints are read-only (GET)
- Ideal for dashboards, analytics, and stakeholder queries

#### Gold Layer Endpoints

##### 1. Hires by Quarter (2021)
Returns the number of employees hired for each job and department in 2021, divided by quarter. Results are ordered alphabetically by department and job.

**Endpoint:**
```bash
GET /api/v1/gold/metrics/hired_by_quarter
```
**Response Example:**
```json
[
  {
    "department": "Accounting",
    "job": "Account Representative IV",
    "q1": 1,
    "q2": 0,
    "q3": 0,
    "q4": 0
  },
  {
    "department": "Engineering",
    "job": "Software Engineer I",
    "q1": 0,
    "q2": 1,
    "q3": 2,
    "q4": 0
  }
]
```

##### 2. Departments Above Mean Hires (2021)
Returns a list of department IDs, names, and number of employees hired for each department that hired more employees than the mean in 2021. Results are ordered by number of hires (descending).

**Endpoint:**
```bash
GET /api/v1/gold/metrics/departments_above_mean
```
**Response Example:**
```json
[
  {"id": 8, "department": "Support", "hired": 217},
  {"id": 5, "department": "Engineering", "hired": 207},
  {"id": 6, "department": "Human Resources", "hired": 204}
]
```

**How it works:**
- These endpoints aggregate and analyze data from the Silver layer tables (`fact_hired_employees`, `dim_departments`, `dim_jobs`).
- They are designed for business reporting and can be consumed by dashboards or analytics tools.

## API Endpoints

> **Note:** To obtain business metrics from the Gold layer, you must first load and transform data through the Bronze and Silver layers.

### Bronze Layer Endpoints
Endpoints for raw data ingestion (CSV uploads):
```bash
POST /api/v1/bronze/upload/departments_csv/
POST /api/v1/bronze/upload/jobs_csv/
POST /api/v1/bronze/upload/hired_employees_csv/
```
**Example Usage:**
```bash
curl -X POST -F "file=@data/departments.csv" http://localhost:8000/api/v1/bronze/upload/departments_csv/
curl -X POST -F "file=@data/jobs.csv" http://localhost:8000/api/v1/bronze/upload/jobs_csv/
curl -X POST -F "file=@data/hired_employees.csv" http://localhost:8000/api/v1/bronze/upload/hired_employees_csv/
```

### Silver Layer Endpoints
Endpoints for transforming and merging data into the dimensional model:
```bash
POST /api/v1/silver/merge/dim_departments/merge
POST /api/v1/silver/merge/dim_jobs/merge
POST /api/v1/silver/merge/fact_hired_employees/merge
```
**Example Usage:**
```bash
curl -X POST http://localhost:8000/api/v1/silver/merge/dim_departments/merge
curl -X POST http://localhost:8000/api/v1/silver/merge/dim_jobs/merge
curl -X POST http://localhost:8000/api/v1/silver/merge/fact_hired_employees/merge
```

### Gold Layer Endpoints
Endpoints for analytics and business metrics:
```bash
GET /api/v1/gold/metrics/hired_by_quarter
GET /api/v1/gold/metrics/departments_above_mean
```
**Example Usage:**
```bash
curl -X GET http://localhost:8000/api/v1/gold/metrics/hired_by_quarter
curl -X GET http://localhost:8000/api/v1/gold/metrics/departments_above_mean
```

## Data Models

### Bronze Layer (Staging Tables)

#### stg_departments
| Column     | Type   | Description        |
|------------|--------|--------------------|
| id         | STRING | Raw department ID  |
| department | STRING | Department name    |

#### stg_jobs
| Column | Type   | Description    |
|--------|--------|----------------|
| id     | STRING | Raw job ID     |
| job    | STRING | Job title      |

#### stg_hired_employees
| Column        | Type   | Description           |
|---------------|--------|-----------------------|
| id            | STRING | Raw employee ID       |
| name          | STRING | Employee name         |
| datetime      | STRING | Hire datetime (ISO)   |
| department_id | STRING | Department reference  |
| job_id        | STRING | Job reference         |

### Silver Layer (Dimensional Model)

#### dim_departments
| Column        | Type         | Constraints | Description        |
|---------------|--------------|-------------|--------------------|
| id_department | INTEGER      | PK          | Department key     |
| department    | VARCHAR(100) | NOT NULL    | Department name    |

#### dim_jobs
| Column  | Type         | Constraints | Description    |
|---------|--------------|-------------|----------------|
| id_job  | INTEGER      | PK          | Job key        |
| job     | VARCHAR(100) | NOT NULL    | Job title      |

#### fact_hired_employees
| Column        | Type         | Constraints | Description        |
|---------------|--------------|-------------|--------------------|
| id_employee   | INTEGER      | PK          | Employee key       |
| name          | VARCHAR(100) | NOT NULL    | Employee name      |
| hire_datetime | TIMESTAMP    | NOT NULL    | Normalized datetime|
| id_department | INTEGER      | FK          | Department key     |
| id_job        | INTEGER      | FK          | Job key           |

### Gold Layer (Analytics & Metrics)

#### Hires by Quarter (2021)
| Field      | Type   | Description                                 |
|------------|--------|---------------------------------------------|
| department | STRING | Department name                             |
| job        | STRING | Job title                                   |
| q1         | INT    | Number of hires in Q1 (Jan-Mar)             |
| q2         | INT    | Number of hires in Q2 (Apr-Jun)             |
| q3         | INT    | Number of hires in Q3 (Jul-Sep)             |
| q4         | INT    | Number of hires in Q4 (Oct-Dec)             |

#### Departments Above Mean Hires (2021)
| Field      | Type   | Description                                 |
|------------|--------|---------------------------------------------|
| id         | INT    | Department ID                               |
| department | STRING | Department name                             |
| hired      | INT    | Number of employees hired in 2021           |

## Project Structure
```
SR_DE_coding_challenge/
├── app/                            # Application package
│   ├── main.py                     # FastAPI application entry point
│   ├── core/                       # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration settings
│   │   └── database.py            # Database connection and session management
│   └── api/                       # API package
│       ├── __init__.py
│       ├── models/                # SQLAlchemy models
│       │   ├── __init__.py        # Model exports
│       │   ├── bronze/           # Staging models
│       │   │   ├── __init__.py
│       │   │   ├── stg_departments.py
│       │   │   ├── stg_jobs.py
│       │   │   └── stg_hired_employees.py
│       │   ├── silver/           # Dimensional models
│       │   │   ├── __init__.py
│       │   │   ├── dim_departments.py
│       │   │   ├── dim_jobs.py
│       │   │   └── fact_hired_employees.py
│       │   └── gold/             # (Optional) Gold models if needed
│       ├── schemas/              # Pydantic schemas
│       │   ├── __init__.py
│       │   ├── base.py           # Base schemas
│       │   ├── department.py     # Department schemas
│       │   ├── job.py           # Job schemas
│       │   ├── hired_employee.py # Employee schemas
│       │   ├── staging.py       # Staging schemas
│       │   └── gold/            # Gold layer schemas
│       │       ├── __init__.py
│       │       └── metrics.py
│       └── routes/              # API endpoints
│           ├── __init__.py      # Router configuration
│           ├── bronze/         # Bronze layer endpoints
│           │   ├── __init__.py
│           │   └── upload/     # Upload endpoints
│           │       ├── __init__.py
│           │       ├── departments_csv.py
│           │       ├── jobs_csv.py
│           │       └── hired_employees_csv.py
│           ├── silver/        # Silver layer endpoints
│           │   ├── __init__.py
│           │   ├── merge/     # Merge endpoints
│           │   │   ├── dim_departments.py
│           │   │   ├── dim_jobs.py
│           │   │   └── fact_hired_employees.py
│           └── gold/         # Gold layer endpoints
│               ├── __init__.py
│               └── metrics.py
├── docker/                     # Docker configuration
│   ├── Dockerfile             # API service Dockerfile
│   └── init.sql              # Database initialization script
├── alembic/                   # Database migrations
│   ├── versions/             # Migration versions
│   │   └── db85176f4d91_create_bronze_and_silver_layers.py
│   ├── env.py               # Alembic environment configuration
│   └── script.py.mako       # Migration script template
├── data/                     # Sample data files
│   ├── departments.csv
│   ├── jobs.csv
│   └── hired_employees.csv
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Docker services configuration
├── alembic.ini              # Alembic configuration
└── README.md                # Project documentation
```

Key Components:
1. Core (/app/core/):
   - config.py: Application settings, environment variables
   - database.py: SQLAlchemy setup, connection management

2. Models (/app/api/models/):
   - Bronze Layer: Raw data models with string fields
   - Silver Layer: Dimensional models with proper data types

3. Schemas (/app/api/schemas/):
   - Data validation and serialization
   - Request/Response models
   - Base schemas for common functionality

4. Routes (/app/api/routes/):
   - Bronze Layer: Data ingestion endpoints for CSV files
   - Silver Layer: Data transformation endpoints

5. Docker:
   - Multi-container setup (API + PostgreSQL)
   - Volume management
   - Network configuration

6. Database:
   - PostgreSQL 15
   - Alembic migrations
   - Initial schema creation

7. Configuration:
   - Environment variables
   - Database settings
   - API settings

## Step by Step Guide

### 1. Initial Setup

1.1. Start the services:
```bash
# Build and start containers
docker-compose build
docker-compose up -d

# Run database migrations
docker-compose exec api alembic upgrade head
```

### 2. Bronze Layer Data Loading

2.1. Load Departments:
```bash
# Upload departments data
curl -X POST \
  -F "file=@data/departments.csv" \
  http://localhost:8000/api/v1/bronze/upload/departments_csv/

# Example Response:
{
    "message": "File processed successfully",
    "rows_processed": 12,
    "status": "success"
}
```

2.2. Load Jobs:
```bash
# Upload jobs data
curl -X POST \
  -F "file=@data/jobs.csv" \
  http://localhost:8000/api/v1/bronze/upload/jobs_csv/

# Example Response:
{
    "message": "File processed successfully",
    "rows_processed": 183,
    "status": "success"
}
```

2.3. Load Hired Employees:
```bash
# Upload hired employees data
curl -X POST \
  -F "file=@data/hired_employees.csv" \
  http://localhost:8000/api/v1/bronze/upload/hired_employees_csv/

# Example Response:
{
    "message": "File processed successfully",
    "rows_processed": 982,
    "status": "success"
}
```

### 3. Silver Layer Transformations

The following describes the transformation and merge endpoints of the Silver layer. Each one performs an upsert (MERGE) operation on the dimensional/fact tables, ensuring data integrity and cleanliness.

#### 3.1. Transform Departments

This endpoint transforms and merges departments from the staging table (`stg_departments`) into the dimensional table (`dim_departments`). It performs inserts and updates as needed, ensuring there are no duplicates and that names are up to date.

**Endpoint:**
```bash
POST /api/v1/silver/merge/dim_departments/merge
```

**Executed SQL:**
```sql
WITH staging_data AS (
    SELECT DISTINCT
        id::integer AS id_department,
        department
    FROM stg_departments
    WHERE id IS NOT NULL
)
MERGE INTO dim_departments AS target
USING staging_data AS source
ON target.id_department = source.id_department
WHEN MATCHED AND target.department IS DISTINCT FROM source.department THEN
    UPDATE SET 
        department = source.department,
        updated_timestamp = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN
    INSERT (id_department, department, created_timestamp, updated_timestamp)
    VALUES (
        source.id_department, 
        source.department,
        CURRENT_TIMESTAMP,
        NULL
    );
```

**Success response:**
```json
{
    "message": "Departments merged successfully",
    "statistics": {
        "initial_count": 0,
        "final_count": 12,
        "total_processed": 12,
        "inserted": 12,
        "updated": 0
    },
    "status": "success"
}
```

**Possible errors:**
- Database error, for example, if there are connection problems or invalid data.

---

#### 3.2. Transform Jobs

This endpoint transforms and merges jobs from the staging table (`stg_jobs`) into the dimensional table (`dim_jobs`).

**Endpoint:**
```bash
POST /api/v1/silver/merge/dim_jobs/merge
```

**Executed SQL:**
```sql
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
```

**Success response:**
```json
{
    "message": "Jobs merged successfully",
    "statistics": {
        "initial_count": 0,
        "final_count": 183,
        "total_processed": 183,
        "inserted": 183,
        "updated": 0
    },
    "status": "success"
}
```

**Possible errors:**
- Database error, for example, if there are connection problems or invalid data.

---

#### 3.3. Transform Hired Employees

This endpoint transforms and merges hired employees from the staging table (`stg_hired_employees`) into the fact table (`fact_hired_employees`). It validates that the department and job IDs exist in the dimensional tables before inserting or updating.

**Endpoint:**
```bash
POST /api/v1/silver/merge/fact_hired_employees/merge
```

**Executed SQL:**
```sql
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
```

**Success response:**
```json
{
    "message": "Hired employees merged successfully",
    "statistics": {
        "initial_count": 0,
        "final_count": 982,
        "total_processed": 982,
        "valid_records": 982,
        "invalid_records": 0
    },
    "status": "success"
}
```

**Possible errors:**
- If there is no data in the staging table:
```json
{
    "detail": {
        "message": "No data found in staging table",
        "hint": "Please load data into stg_hired_employees before attempting merge"
    }
}
```
- If an unexpected error occurs:
```json
{
    "detail": {
        "message": "Error during merge operation",
        "error": "<error details>",
        "hint": "Check validation details for specific issues"
    }
}
```

---

**Important notes:**
- Run the merges in the following order: first departments, then jobs, and finally hired employees, to ensure referential integrity.
- Merges are idempotent and can be repeated without risk of duplicates.
- It is recommended to review the returned statistics to monitor inserts and updates.

### 4. Verification and Monitoring

4.1. Check API Status:
```bash
# Verify API is running
curl http://localhost:8000/health

# Example Response:
{
    "status": "healthy",
    "version": "1.0.0"
}
```

4.2. View API Documentation:
```bash
# Open in your browser:
http://localhost:8000/docs  # Swagger UI
http://localhost:8000/redoc # ReDoc
```

### 5. Error Handling

The API provides detailed error messages for common scenarios:

5.1. File Format Errors:
```json
{
    "detail": "Invalid file format. Please provide a CSV file.",
    "status": "error"
}
```

5.2. Data Validation Errors:
```json
{
    "detail": "Row 5: Invalid datetime format. Expected ISO format.",
    "status": "error",
    "row": 5,
    "column": "datetime"
}
```

5.3. Database Errors:
```json
{
    "detail": "Foreign key violation. Department ID not found.",
    "status": "error",
    "constraint": "fk_department_id"
}
```

### 6. Best Practices

1. **Order of Operations:**
   - Always load dimension tables (departments, jobs) before fact tables
   - Transform dimensions before facts
   - Verify row counts after each operation

2. **Data Validation:**
   - Check file formats before upload
   - Validate data types match expected schema
   - Ensure referential integrity

3. **Monitoring:**
   - Track statistics after each operation
   - Monitor database performance
   - Check logs for errors

4. **Recovery:**
   - Operations are idempotent
   - Can safely retry failed operations
   - Use transaction rollback for consistency

### 7. Troubleshooting

Common issues and solutions:

1. **Connection Errors:**
```bash
# Check if containers are running
docker-compose ps

# Check container logs
docker-compose logs api
docker-compose logs db
```

2. **Database Issues:**
```bash
# Reset database (if needed)
docker-compose down -v
docker-compose up -d
docker-compose exec api alembic upgrade head
```

3. **Permission Issues:**
```bash
# Fix file permissions
chmod 644 data/*.csv
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[License Information]