# SR_DE_coding_challenge

## Project Overview
This project implements a data migration API following a two-layer medallion architecture for efficient data processing and analytics. It provides endpoints for data ingestion, transformation, and dimensional modeling.

## Architecture
The project follows a medallion architecture with two layers:

### Bronze Layer (Staging)
- Raw data ingestion layer
- Preserves source data in its original form
- All fields stored as strings
- Includes data quality tracking
- Tables prefixed with 'stg_'
- Bulk upload functionality with batch processing
- Data validation and error reporting

### Silver Layer (Dimensional Model)
- Clean, validated data
- Proper data types and constraints
- Dimensional modeling (star schema)
- Business rules implemented
- Tables prefixed with 'dim_' for dimensions and 'fact_' for facts
- MERGE operations with detailed statistics
- Referential integrity enforcement

## Process Flow
1. Data Ingestion (Bronze Layer):
   - Upload CSV files to staging tables
   - Basic validation (file format, column count)
   - Batch processing for large files
   - Error tracking and reporting
   - Endpoints:
     - `/api/v1/bronze/upload/departments/`
     - `/api/v1/bronze/upload/jobs/`
     - `/api/v1/bronze/upload/hired_employees/`

2. Data Transformation (Silver Layer):
   - Transform staging data to dimensional model
   - Data type conversion and validation
   - MERGE operations (upsert)
   - Statistics tracking
   - Endpoints:
     - `/api/v1/silver/departments/merge`
     - `/api/v1/silver/jobs/merge`
     - `/api/v1/silver/hired_employees/merge`

## Data Models

### Bronze Layer Tables

#### stg_departments
- `id` STRING - Raw department ID
- `department` STRING - Department name

#### stg_jobs
- `id` STRING - Raw job ID
- `job` STRING - Job title

#### stg_hired_employees
- `id` STRING - Raw employee ID
- `name` STRING - Employee name
- `datetime` STRING - Hire datetime in ISO format
- `department_id` STRING - Reference to department
- `job_id` STRING - Reference to job

### Silver Layer Tables

#### dim_departments
- `id_department` INTEGER (PK) - Department surrogate key
- `department` VARCHAR(100) - Department name

#### dim_jobs
- `id_job` INTEGER (PK) - Job surrogate key
- `job` VARCHAR(100) - Job title

#### fact_hired_employees
- `id_employee` INTEGER (PK) - Employee surrogate key
- `name` VARCHAR(100) - Employee name
- `hire_datetime` TIMESTAMP - Normalized hire datetime
- `id_department` INTEGER (FK) - Reference to dim_departments
- `id_job` INTEGER (FK) - Reference to dim_jobs

## Setup and Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Start services: `docker-compose up -d`
4. Access API documentation: `http://localhost:8000/docs`

## API Documentation
The API documentation is available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Example Usage

### 1. Upload Departments to Bronze Layer
```bash
curl -X POST -F "file=@data/departments.csv" http://localhost:8000/api/v1/bronze/upload/departments/
```

### 2. Transform to Silver Layer
```bash
curl -X POST http://localhost:8000/api/v1/silver/departments/merge
```

The response includes detailed statistics about the operation:
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

## Technologies Used
- FastAPI: Modern web framework for building APIs
- PostgreSQL 15: Database with native MERGE support
- SQLAlchemy: SQL toolkit and ORM
- Docker: Containerization
- Alembic: Database migrations
- Pydantic: Data validation

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
│       │   └── silver/           # Dimensional models
│       │       ├── __init__.py
│       │       ├── dim_departments.py
│       │       ├── dim_jobs.py
│       │       └── fact_hired_employees.py
│       ├── schemas/              # Pydantic schemas
│       │   ├── __init__.py
│       │   ├── base.py           # Base schemas
│       │   ├── department.py     # Department schemas
│       │   ├── job.py           # Job schemas
│       │   ├── hired_employee.py # Employee schemas
│       │   └── staging.py       # Staging schemas
│       └── routes/              # API endpoints
│           ├── __init__.py      # Router configuration
│           ├── bronze/         # Bronze layer endpoints
│           │   ├── __init__.py
│           │   └── upload/     # Upload endpoints
│           │       ├── __init__.py
│           │       ├── departments.py
│           │       ├── jobs.py
│           │       └── hired_employees.py
│           └── silver/        # Silver layer endpoints
│               ├── __init__.py
│               ├── dim_departments.py
│               ├── dim_jobs.py
│               └── fact_hired_employees.py
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
   - Bronze Layer: Data ingestion endpoints
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
  http://localhost:8000/api/v1/bronze/upload/departments/

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
  http://localhost:8000/api/v1/bronze/upload/jobs/

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
  http://localhost:8000/api/v1/bronze/upload/hired_employees/

# Example Response:
{
    "message": "File processed successfully",
    "rows_processed": 982,
    "status": "success"
}
```

### 3. Silver Layer Transformations

3.1. Transform Departments:
```bash
# Transform departments to dimensional model
curl -X POST http://localhost:8000/api/v1/silver/departments/merge

# Example Response:
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

3.2. Transform Jobs:
```bash
# Transform jobs to dimensional model
curl -X POST http://localhost:8000/api/v1/silver/jobs/merge

# Example Response:
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

3.3. Transform Hired Employees:
```bash
# Transform hired employees to fact table
curl -X POST http://localhost:8000/api/v1/silver/hired_employees/merge

# Example Response:
{
    "message": "Hired employees merged successfully",
    "statistics": {
        "initial_count": 0,
        "final_count": 982,
        "total_processed": 982,
        "inserted": 982,
        "updated": 0
    },
    "status": "success"
}
```

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