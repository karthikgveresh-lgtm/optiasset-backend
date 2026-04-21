"""
Database Configuration Module

This module sets up the SQLAlchemy database engine and session maker.
It uses an SQLite database for ease of setup and testing without needing a standalone MySQL server.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./asset_tracker.db"

# Create the SQLAlchemy engine. 
# check_same_thread=False is needed for SQLite to allow multiple threads (FastAPI) to access the DB
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class. Each instance of this class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our SQLAlchemy ORM models
Base = declarative_base()

def get_db():
    """
    Dependency function to yield a database session.
    Ensures the session is closed after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
