"""
Database configuration module for the Globant Data Migration API.

This module sets up the SQLAlchemy engine, session management, and base model class.
It provides the core database functionality used throughout the application.

Functions:
    get_db: Dependency function to get a database session.

Variables:
    engine: SQLAlchemy database engine instance
    session_local: SQLAlchemy session factory
    base: Declarative base class for database models
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    # Additional engine configuration can be added here
    pool_pre_ping=True,  # Enable connection pool "pre-ping" feature
)

# Create session factory
session_local = sessionmaker(
    autocommit=False,  # Transactions must be committed explicitly
    autoflush=False,   # Changes won't be automatically flushed
    bind=engine        # Bind to our database engine
)

# Create declarative base class for models
base = declarative_base()

def get_db():
    """
    Dependency function to get a database session.
    
    This function creates a new SQLAlchemy session and ensures it is properly
    closed after use, even if an exception occurs during the request.
    
    Yields:
        Session: SQLAlchemy database session
    
    Example:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = session_local()
    try:
        yield db
    finally:
        db.close()
