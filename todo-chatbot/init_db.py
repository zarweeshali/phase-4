"""
Database initialization script for Phase 4 system
Creates all tables based on models
"""

from database.connection import engine
from models.task import Base


def init_db():
    """
    Initialize the database by creating all tables
    """
    print("Initializing Phase 4 database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")
    print("All persistent state will live in the database as per Phase 4 constitution.")


if __name__ == "__main__":
    init_db()