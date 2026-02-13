"""
MCP Tools for Phase 4 Todo AI Chatbot
Following the specification for task operations
"""

from sqlmodel import Session, select
from backend.models.v2.models import Task, TaskStatus
from typing import List, Optional
from datetime import datetime


def add_task(session: Session, user_id: str, title: str, description: Optional[str] = None) -> dict:
    """
    MCP Tool: add_task
    Purpose: Create a new task
    Parameters: user_id (string, required), title (string, required), description (string, optional)
    Returns: task_id, status, title
    """
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        status=TaskStatus.pending,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return {
        "task_id": task.id,
        "status": "created",
        "title": task.title
    }


def list_tasks(session: Session, user_id: str, status: Optional[str] = "all") -> List[dict]:
    """
    MCP Tool: list_tasks
    Purpose: Retrieve tasks from the list
    Parameters: user_id (string, required), status (string, optional: "all", "pending", "completed")
    Returns: Array of task objects
    """
    query = select(Task).where(Task.user_id == user_id)
    
    if status and status != "all":
        if status == "completed":
            query = query.where(Task.status == TaskStatus.completed)
        elif status == "pending":
            query = query.where(Task.status == TaskStatus.pending)
        elif status == "in_progress":
            query = query.where(Task.status == TaskStatus.in_progress)
    
    tasks = session.exec(query).all()
    
    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status.value,
            "completed": task.status == TaskStatus.completed
        }
        for task in tasks
    ]


def complete_task(session: Session, user_id: str, task_id: int) -> dict:
    """
    MCP Tool: complete_task
    Purpose: Mark a task as complete
    Parameters: user_id (string, required), task_id (integer, required)
    Returns: task_id, status, title
    """
    task = session.get(Task, task_id)
    
    if not task:
        return {
            "task_id": task_id,
            "status": "error",
            "title": "Task not found",
            "error": "Task not found"
        }
    
    if task.user_id != user_id:
        return {
            "task_id": task_id,
            "status": "error",
            "title": "Unauthorized",
            "error": "You don't have permission to modify this task"
        }
    
    task.status = TaskStatus.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return {
        "task_id": task.id,
        "status": "completed",
        "title": task.title
    }


def delete_task(session: Session, user_id: str, task_id: int) -> dict:
    """
    MCP Tool: delete_task
    Purpose: Remove a task from the list
    Parameters: user_id (string, required), task_id (integer, required)
    Returns: task_id, status, title
    """
    task = session.get(Task, task_id)
    
    if not task:
        return {
            "task_id": task_id,
            "status": "error",
            "title": "Task not found",
            "error": "Task not found"
        }
    
    if task.user_id != user_id:
        return {
            "task_id": task_id,
            "status": "error",
            "title": "Unauthorized",
            "error": "You don't have permission to delete this task"
        }
    
    title = task.title
    session.delete(task)
    session.commit()
    
    return {
        "task_id": task_id,
        "status": "deleted",
        "title": title
    }


def update_task(session: Session, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> dict:
    """
    MCP Tool: update_task
    Purpose: Modify task title or description
    Parameters: user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional)
    Returns: task_id, status, title
    """
    task = session.get(Task, task_id)
    
    if not task:
        return {
            "task_id": task_id,
            "status": "error",
            "title": "Task not found",
            "error": "Task not found"
        }
    
    if task.user_id != user_id:
        return {
            "task_id": task_id,
            "status": "error",
            "title": "Unauthorized",
            "error": "You don't have permission to modify this task"
        }
    
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return {
        "task_id": task.id,
        "status": "updated",
        "title": task.title
    }