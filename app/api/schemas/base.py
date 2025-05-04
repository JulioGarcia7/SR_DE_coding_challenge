"""
Base schemas module.

This module contains base Pydantic models and common configurations for all schemas.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    """Base schema with common configurations."""
    model_config = ConfigDict(from_attributes=True)

class TimestampMixin(BaseModel):
    """Mixin to add timestamp fields to schemas."""
    created_at: datetime | None = None
    updated_at: datetime | None = None 