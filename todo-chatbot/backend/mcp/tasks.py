"""
MCP Tools Module for Backend
Following Phase 4 constitution:
- MCP tools are stateless
- MCP tools are deterministic
- MCP tools are database-only
- MCP tools contain no AI logic and no memory
- MCP tools are the only way to create, update, or delete tasks

Following Spec-4: Authentication & Authorization
- Each todo is linked to a single user
"""

from sqlalchemy.orm import Session
from backend.models.task import Task
from typing import List, Optional


def create_task(db: Session, title: str, description: str, user_id: int) -> Task:
    """
    MCP Tool to create a task
    Stateless, deterministic, database-only
    Following Spec-4: Each todo is linked to a single user
    """
    db_task = Task(title=title, description=description, user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int) -> Optional[Task]:
    """
    MCP Tool to get a task by ID
    Stateless, deterministic, database-only
    """
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks_by_user(db: Session, user_id: int) -> List[Task]:
    """
    MCP Tool to get all tasks for a user
    Stateless, deterministic, database-only
    Following Spec-4: Each todo is linked to a single user
    """
    return db.query(Task).filter(Task.user_id == user_id).all()


def update_task_status(db: Session, task_id: int, status: str) -> Optional[Task]:
    """
    MCP Tool to update task status
    Stateless, deterministic, database-only
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = status
        db.commit()
        db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> bool:
    """
    MCP Tool to delete a task
    Stateless, deterministic, database-only
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False