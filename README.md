# SR_DE_coding_challenge

## Project Overview
This project implements a data migration API following a two-layer medallion architecture for efficient data processing and analytics. The system processes employee hiring data through a robust ETL pipeline, transforming raw CSV data into a dimensional model suitable for analysis.

## Architecture Flow Diagram
```
[Inicio] → [Archivos CSV]
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
            
    ↓ [Transformación y Validación]
    
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
            
    ↓ [Análisis y Reportes]
    
[API Endpoints]
    │
    ├─→ [Bronze Layer API]
    │       POST /api/v1/bronze/upload/{entity}/
    │
    └─→ [Silver Layer API]
            POST /api/v1/silver/{entity}/merge
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

## API Endpoints

### Bronze Layer Endpoints
Upload endpoints for raw data ingestion:
```bash
POST /api/v1/bronze/upload/departments_csv/
POST /api/v1/bronze/upload/jobs_csv/
POST /api/v1/bronze/upload/hired_employees_csv/
```

### Silver Layer Endpoints
Transformation endpoints for dimensional modeling:
```bash
POST /api/v1/silver/departments/merge
POST /api/v1/silver/jobs/merge
POST /api/v1/silver/hired_employees/merge
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

## Setup and Installation

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- PostgreSQL 15

### Quick Start
1. Clone the repository:
```bash
git clone [repository-url]
cd SR_DE_coding_challenge
```

2. Start services:
```bash
docker-compose up -d
```

3. Run migrations:
```bash
docker-compose exec api alembic upgrade head
```

4. Access the API:
- API Documentation: http://localhost:8000/docs
- ReDoc Interface: http://localhost:8000/redoc

## Example Usage

### 1. Upload Department Data
```bash
curl -X POST \
  -F "file=@data/departments.csv" \
  http://localhost:8000/api/v1/bronze/upload/departments_csv/
```

### 2. Transform to Dimensional Model
```bash
curl -X POST \
  http://localhost:8000/api/v1/silver/departments/merge
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
- FastAPI: Modern, high-performance web framework
- PostgreSQL 15: Advanced relational database
- SQLAlchemy: SQL toolkit and ORM
- Alembic: Database migration tool
- Docker & Docker Compose: Containerization
- Pydantic: Data validation
- Python 3.8+: Programming language

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
│           │       ├── departments_csv.py
│           │       ├── jobs_csv.py
│           │       └── hired_employees_csv.py
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

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[License Information]