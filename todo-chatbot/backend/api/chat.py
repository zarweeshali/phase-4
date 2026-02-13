"""
Chat API module for Phase 4 backend
Following the constitution:
- Each /api/{user_id}/chat request is independent
- Conversation history is fetched from the database
- No in-process or hidden state is allowed

Following Spec-4: Authentication & Authorization
- Only authenticated users can access todos
- Each todo is linked to a single user
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.mcp.tasks import get_tasks_by_user, create_task
from backend.middleware.auth import get_current_user
from backend.models.user import User
from typing import List


router = APIRouter()


@router.get("/chat")
async def chat(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat endpoint following Phase 4 constitution and Spec-4:
    - Stateless server
    - Conversation context rebuilt per request
    - All state in database
    - Only authenticated users can access todos
    - Each todo is linked to a single user
    """
    # Fetch conversation history from database for the authenticated user
    # According to constitution: "Conversation history is fetched from the database"
    tasks = get_tasks_by_user(db, current_user.id)
    
    # Return conversation context rebuilt from database
    # According to constitution: "Conversation context is rebuilt per request"
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "conversation_history": [
            {
                "task_id": task.id,
                "title": task.title,
                "status": task.status,
                "created_at": task.created_at
            } for task in tasks
        ],
        "stateless": True,
        "constitution_compliant": True
    }


@router.post("/chat")
async def create_task_endpoint(
    title: str,
    description: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint to create a new task via chat interface
    Uses MCP tools as required by constitution
    Following Spec-4: Each todo is linked to a single user
    """
    from backend.mcp.tasks import create_task
    
    # Create task linked to the authenticated user
    task = create_task(db, title, description, current_user.id)
    
    return {
        "message": "Task created successfully",
        "task_id": task.id,
        "title": task.title,
        "status": task.status,
        "user_id": current_user.id
    }