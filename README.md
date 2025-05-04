# SR_DE_coding_challenge

## Project Overview
This project implements a data migration API following a two-layer medallion architecture for efficient data processing and analytics.

## Architecture
The project follows a medallion architecture with two layers:

### Bronze Layer (Staging)
- Raw data ingestion layer
- Preserves source data in its original form
- All fields stored as strings
- Includes data quality tracking
- Tables prefixed with 'stg_'

### Silver Layer (Dimensional Model)
- Clean, validated data
- Proper data types and constraints
- Dimensional modeling (star schema)
- Business rules implemented
- Tables prefixed with 'dim_' for dimensions and 'fact_' for facts

## Data Models

### CSV Files Structure

#### hired_employees.csv
- `id` INTEGER - Id of the employee
- `name` STRING - Name and surname of the employee
- `datetime` STRING - Hire datetime in ISO format
- `department_id` INTEGER - Id of the department which the employee was hired for
- `job_id` INTEGER - Id of the job which the employee was hired for

Example:
```
4535,Marcelo Gonzalez,2021-07-27T16:02:08Z,1,2
4572,Lidia Mendez,2021-07-27T19:04:09Z,1,2
```

#### departments.csv
- `id` INTEGER - Id of the department
- `department` STRING - Name of the department

Example:
```
1,Supply Chain
2,Maintenance
3,Staff
```

#### jobs.csv
- `id` INTEGER - Id of the job
- `job` STRING - Name of the job

Example:
```
1,Recruiter
2,Manager
3,Analyst
```

## Project Structure
```
SR_DE_coding_challenge/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── core/               # Core configurations
│   └── api/
│       ├── models/         # Database models
│       │   ├── bronze/    # Staging models
│       │   └── silver/    # Dimensional models
│       ├── schemas/        # Pydantic schemas
│       └── routes/         # API endpoints
├── docker/                 # Docker configuration
└── requirements.txt        # Python dependencies
```

## Setup and Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Start services: `docker-compose up -d`
4. Access API documentation: `http://localhost:8000/docs`

## API Documentation
The API documentation is available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`