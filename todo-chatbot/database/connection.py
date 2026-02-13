"""
Database connection module for Phase 4 system
All persistent state lives in the database
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# Using SQLite for simplicity, but can be changed to PostgreSQL, MySQL, etc.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./phase4.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency to get database session
    Following Phase 4 constitution - all state in DB
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()