"""
Database connection module for Phase 4 Todo AI Chatbot
Using SQLModel and Neon PostgreSQL
"""

from sqlmodel import create_engine, Session
from typing import Generator
import os


# Using Neon PostgreSQL - in production, this would come from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/dbname")

# For development, we'll use a fallback to SQLite
if "localhost" in DATABASE_URL or "username:password" in DATABASE_URL:
    DATABASE_URL = "sqlite:///./phase4_chatbot.db"

engine = create_engine(DATABASE_URL)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    Following Phase 4 constitution - all state in DB
    """
    with Session(engine) as session:
        yield session