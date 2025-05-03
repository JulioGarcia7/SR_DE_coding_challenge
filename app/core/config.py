"""
Configuration module for the Globant Data Migration API.

This module handles all the configuration settings for the application using Pydantic's BaseSettings.
It loads configuration from environment variables and provides default values when needed.

Classes:
    Settings: Main configuration class that inherits from BaseSettings.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Settings class for application configuration.
    
    This class uses Pydantic's BaseSettings to handle configuration variables.
    It will attempt to load values from environment variables first, then fall back to defaults.
    
    Attributes:
        database_url (str): PostgreSQL connection string. Format:
            postgresql://<user>:<password>@<host>:<port>/<database>
        api_v1_str (str): API version prefix for all endpoints
        project_name (str): Name of the project, used in API documentation
    """
    
    # Database settings
    database_url: str = "postgresql://globant_user:globant_password@db:5432/globant_migration_db"
    
    # API Settings
    api_v1_str: str = "/api/v1"
    project_name: str = "Globant Data Migration API"
    
    class Config:
        """Pydantic configuration class"""
        case_sensitive = True

# Create a global settings object
settings = Settings()
