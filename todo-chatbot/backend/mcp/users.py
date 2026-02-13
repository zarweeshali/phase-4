"""
MCP Tools Module for Users
Following Phase 4 constitution:
- MCP tools are stateless
- MCP tools are deterministic
- MCP tools are database-only
- MCP tools contain no AI logic and no memory
- MCP tools are the only way to create, update, or delete users
"""

from sqlalchemy.orm import Session
from backend.models.user import User, get_password_hash, verify_password
from typing import Optional


def create_user(db: Session, email: str, password: str) -> User:
    """
    MCP Tool to create a user
    Stateless, deterministic, database-only
    Passwords are hashed as required by Spec-4
    """
    hashed_password = get_password_hash(password)
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    MCP Tool to get a user by email
    Stateless, deterministic, database-only
    """
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    MCP Tool to authenticate a user
    Verifies credentials and returns user if valid
    """
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    MCP Tool to get a user by ID
    Stateless, deterministic, database-only
    """
    return db.query(User).filter(User.id == user_id).first()