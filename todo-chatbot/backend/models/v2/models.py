"""
Database models for Phase 4 Todo AI Chatbot
Using SQLModel for the ORM
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class Task(SQLModel, table=True):
    """
    Task model representing todo items
    Following the specification: user_id, id, title, description, completed, created_at, updated_at
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Changed from int to str to match spec
    title: str
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.pending)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class Conversation(SQLModel, table=True):
    """
    Conversation model representing chat sessions
    Following the specification: user_id, id, created_at, updated_at
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class Message(SQLModel, table=True):
    """
    Message model representing chat history
    Following the specification: user_id, id, conversation_id, role (user/assistant), content, created_at
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: int = Field(index=True)  # Removed foreign key constraint for simplicity
    role: MessageRole
    content: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)