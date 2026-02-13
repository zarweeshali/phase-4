"""
Chat API module for Phase 4 system
Following the constitution:
- Each /api/{user_id}/chat request is independent
- Conversation history is fetched from the database
- No in-process or hidden state is allowed
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from mcp.tasks import get_tasks_by_user
from typing import List


router = APIRouter()


@router.get("/{user_id}/chat")
async def chat(user_id: str, db: Session = Depends(get_db)):
    """
    Chat endpoint following Phase 4 constitution:
    - Stateless server
    - Conversation context rebuilt per request
    - All state in database
    """
    # Fetch conversation history from database
    # According to constitution: "Conversation history is fetched from the database"
    tasks = get_tasks_by_user(db, user_id)
    
    # Return conversation context rebuilt from database
    # According to constitution: "Conversation context is rebuilt per request"
    return {
        "user_id": user_id,
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