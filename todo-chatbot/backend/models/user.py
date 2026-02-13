"""
User model for Phase 4 system
Following the constitution: All persistent state lives in the database
MCP tools are the only way to create, update, or delete users
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.database.connection import Base
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """
    User model following Phase 4 constitution
    MCP tools are the only way to create, update, or delete users
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


def verify_password(plain_password, hashed_password):
    """Verify plain password against hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Generate hash for plain password"""
    return pwd_context.hash(password)