"""
Base schemas module.

This module contains base Pydantic models and common configurations for all schemas.
"""

from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    """Base schema with common configurations."""
    model_config = ConfigDict(from_attributes=True) 