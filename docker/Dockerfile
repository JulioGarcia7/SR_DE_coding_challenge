# Use a lightweight official Python base image.
FROM python:3.11-slim

# Set the working directory in the container to /app.
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        python3-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app.
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app.
COPY . .

# Create necessary directories if they don't exist
RUN mkdir -p /app/data

# Make sure the application user owns the files
RUN chown -R nobody:nogroup /app

# Switch to non-root user
USER nobody

# Expose port 8000 for the application.
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 