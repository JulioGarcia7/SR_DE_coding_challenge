"""
Tests for the hired employees upload endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from io import StringIO
import csv

from app.main import app
from app.core.database import get_db, base, engine
from app.api.models.bronze.stg_hired_employees import StgHiredEmployees

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

# Test uploading valid hired employee data
def test_upload_valid_data(test_db):
    test_data = [
        [1, "John Doe", "2021-01-01T00:00:00Z", 1, 1],
        [2, "Jane Smith", "2021-01-02T00:00:00Z", 2, 2]
    ]
    csv_file = create_test_csv(test_data)
    response = client.post(
        "/api/v1/bronze/upload/hired_employees_csv/",
        files={"file": ("test.csv", csv_file.getvalue(), "text/csv")}
    )
    assert response.status_code == 201
    assert response.json()["total_processed"] == 2
    assert response.json()["total_batches"] == 1
    assert len(response.json()["errors"]) == 0

# Test uploading hired employee data with null or empty values
def test_upload_with_null_values(test_db):
    test_data = [
        [1, "John Doe", "2021-01-01T00:00:00Z", "", 1],
        [2, "", "2021-01-02T00:00:00Z", 2, 2],
        [3, "Jane Smith", "", 3, 3],
        [4, "Bob Wilson", "2021-01-04T00:00:00Z", 4, ""]
    ]
    csv_file = create_test_csv(test_data)
    response = client.post(
        "/api/v1/bronze/upload/hired_employees_csv/",
        files={"file": ("test.csv", csv_file.getvalue(), "text/csv")}
    )
    assert response.status_code == 201
    assert isinstance(response.json()["errors"], list)

# Test handling of invalid date formats in hired employees
def test_upload_invalid_date_format(test_db):
    test_data = [
        [1, "John Doe", "2021-13-01T00:00:00Z", 1, 1],
        [2, "Jane Smith", "2021-01-32T00:00:00Z", 2, 2],
        [3, "Bob Wilson", "invalid_date", 3, 3]
    ]
    csv_file = create_test_csv(test_data)
    response = client.post(
        "/api/v1/bronze/upload/hired_employees_csv/",
        files={"file": ("test.csv", csv_file.getvalue(), "text/csv")}
    )
    assert response.status_code == 201
    assert len(response.json()["errors"]) == 3
    for error in response.json()["errors"]:
        assert "datetime" in error["error"].lower()

# Test that batch processing works for more than 1000 rows
def test_upload_batch_size_limit(test_db):
    test_data = [
        [i, f"Employee {i}", "2021-01-01T00:00:00Z", 1, 1]
        for i in range(1, 1501)
    ]
    csv_file = create_test_csv(test_data)
    response = client.post(
        "/api/v1/bronze/upload/hired_employees_csv/",
        files={"file": ("test.csv", csv_file.getvalue(), "text/csv")}
    )
    assert response.status_code == 201
    assert response.json()["total_processed"] == 1500
    assert response.json()["total_batches"] == 2

# Test rejection of non-CSV file formats
def test_upload_invalid_file_format(test_db):
    response = client.post(
        "/api/v1/bronze/upload/hired_employees_csv/",
        files={"file": ("test.txt", "invalid content", "text/plain")}
    )
    assert response.status_code == 400
    assert "CSV" in response.json()["detail"]

# Test handling of rows with invalid column count
def test_upload_invalid_column_count(test_db):
    test_data = [
        [1, "John Doe", "2021-01-01T00:00:00Z", 1],
        [2, "Jane Smith", "2021-01-02T00:00:00Z", 2, 2, "extra"],
    ]
    csv_file = create_test_csv(test_data)
    response = client.post(
        "/api/v1/bronze/upload/hired_employees_csv/",
        files={"file": ("test.csv", csv_file.getvalue(), "text/csv")}
    )
    assert response.status_code == 201
    assert len(response.json()["errors"]) == 2
    for error in response.json()["errors"]:
        assert "Invalid number of columns" in error["error"] 