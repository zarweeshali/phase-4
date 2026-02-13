"""
Database initialization script for Phase 4 backend system
Creates all tables based on models
"""

from backend.database.connection import engine
from backend.models.task import Base as TaskBase
from backend.models.user import Base as UserBase


def init_db():
    """
    Initialize the database by creating all tables
    """
    print("Initializing Phase 4 backend database...")
    TaskBase.metadata.create_all(bind=engine)
    UserBase.metadata.create_all(bind=engine)
    print("Backend database initialized successfully!")
    print("All persistent state will live in the database as per Phase 4 constitution.")


if __name__ == "__main__":
    init_db()