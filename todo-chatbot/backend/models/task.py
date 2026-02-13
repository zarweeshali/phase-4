"""
Models for Phase 4 backend system
All persistent state lives in the database
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.connection import Base


class Task(Base):
    """
    Task model following Phase 4 constitution
    MCP tools are the only way to create, update, or delete tasks
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="pending")  # pending, in_progress, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), index=True)  # Associated user
    
    # Relationship to user
    user = relationship("User", back_populates="tasks")


from .user import User
User.tasks = relationship("Task", order_by=Task.id, back_populates="user")