"""
Tests for the departments upload endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from io import StringIO
import csv

from app.main import app
from app.core.database import get_db, base, engine
from app.api.models.bronze.stg_departments import StgDepartments

client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    """Create test database tables before each test and drop them after."""
    base.metadata.create_all(bind=engine)
    yield
    base.metadata.drop_all(bind=engine)

def create_test_csv(data: list) -> StringIO:
    """Create a CSV file in memory from test data."""
    output = StringIO()
    writer = csv.writer(output)
    for row in data:
        writer.writerow(row)
    output.seek(0)
    return output

def test_upload_valid_data(test_db):
    """Test uploading valid department data."""
    test_data = [
        [1, "Sales"],
        [2, "Marketing"],
        [3, "Engineering"]
    ]
    csv_file = create_test_csv(test_data)
    
    response = client.post(
        "/api/v1/bronze/upload/departments_csv/",
        files={"file": ("test.csv", csv_file.getvalue(), "text/csv")}
    )
    
    assert response.status_code == 201
    assert response.json()["total_processed"] == 3
    assert response.json()["total_batches"] == 1
    assert len(response.json()["errors"]) == 0

def test_upload_with_null_values(test_db):
    """Test handling of null values in CSV."""
    test_data = [
        [1, ""],  # Empty department name
        ["", "Marketing"],  # Empty id
        [3, None]  # None value
    ]
    csv_file = create_test_csv(test_data)
    
    response = client.post(
        "/api/v1/bronze/upload/departments_csv/",
        files={"file": ("test.csv", csv_file.getvalue(), "text/csv")}
    )
    
    assert response.status_code == 201
    assert len(response.json()["errors"]) > 0
    assert "Missing required field" in str(response.json()["errors"])

def test_upload_batch_size_limit(test_db):
    """Test that files are processed in batches of 1000 rows."""
    # Create 1500 rows of test data
    test_data = [
        [i, f"Department {i}"]
        for i in range(1, 1501)
    ]
    csv_file = create_test_csv(test_data)
    
    response = client.post(
        "/api/v1/bronze/upload/departments_csv/",
        files={"file": ("test.csv", csv_file.getvalue(), "text/csv")}
    )
    
    assert response.status_code == 201
    assert response.json()["total_processed"] == 1500
    assert response.json()["total_batches"] == 2  # Should be split into 2 batches

def test_upload_invalid_file_format(test_db):
    """Test handling of invalid file format."""
    response = client.post(
        "/api/v1/bronze/upload/departments_csv/",
        files={"file": ("test.txt", "invalid content", "text/plain")}
    )
    
    assert response.status_code == 400
    assert "Only CSV files are allowed" in response.json()["detail"]

def test_upload_invalid_column_count(test_db):
    """Test handling of invalid column count in CSV."""
    test_data = [
        [1, "Sales", "Extra Column"],  # Too many columns
        [2],  # Too few columns
    ]
    csv_file = create_test_csv(test_data)
    
    response = client.post(
        "/api/v1/bronze/upload/departments_csv/",
        files={"file": ("test.csv", csv_file.getvalue(), "text/csv")}
    )
    
    assert response.status_code == 201
    assert "Invalid number of columns" in str(response.json()["errors"]) 