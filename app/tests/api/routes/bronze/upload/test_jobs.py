"""
Tests for the jobs upload endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from io import StringIO
import csv

from app.main import app
from app.core.database import get_db, base, engine
from app.api.models.bronze.stg_jobs import StgJobs

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

# Test uploading valid job data
def test_upload_valid_data(test_db):
    test_data = [
        [1, "Software Engineer"],
        [2, "Data Scientist"],
        [3, "Product Manager"]
    ]
    csv_file = create_test_csv(test_data)
    response = client.post(
        "/api/v1/bronze/upload/jobs_csv/",
        files={"file": ("test.csv", csv_file.getvalue(), "text/csv")}
    )
    assert response.status_code == 201
    assert response.json()["total_processed"] == 3
    assert response.json()["total_batches"] == 1
    assert len(response.json()["errors"]) == 0

# Test uploading job data with null or empty values
def test_upload_with_null_values(test_db):
    test_data = [
        [1, ""],
        ["", "Data Engineer"],
        [3, None]
    ]
    csv_file = create_test_csv(test_data)
    response = client.post(
        "/api/v1/bronze/upload/jobs_csv/",
        files={"file": ("test.csv", csv_file.getvalue(), "text/csv")}
    )
    assert response.status_code == 201
    assert isinstance(response.json()["errors"], list)

# Test that batch processing works for more than 1000 rows
def test_upload_batch_size_limit(test_db):
    test_data = [
        [i, f"Job {i}"]
        for i in range(1, 1501)
    ]
    csv_file = create_test_csv(test_data)
    response = client.post(
        "/api/v1/bronze/upload/jobs_csv/",
        files={"file": ("test.csv", csv_file.getvalue(), "text/csv")}
    )
    assert response.status_code == 201
    assert response.json()["total_processed"] == 1500
    assert response.json()["total_batches"] == 2

# Test rejection of non-CSV file formats
def test_upload_invalid_file_format(test_db):
    response = client.post(
        "/api/v1/bronze/upload/jobs_csv/",
        files={"file": ("test.txt", "invalid content", "text/plain")}
    )
    assert response.status_code == 400
    assert "Only CSV files are allowed" in response.json()["detail"]

# Test handling of rows with invalid column count
def test_upload_invalid_column_count(test_db):
    test_data = [
        [1, "Engineer", "Extra Column"],
        [2],
    ]
    csv_file = create_test_csv(test_data)
    response = client.post(
        "/api/v1/bronze/upload/jobs_csv/",
        files={"file": ("test.csv", csv_file.getvalue(), "text/csv")}
    )
    assert response.status_code == 201
    assert "Invalid number of columns" in str(response.json()) 