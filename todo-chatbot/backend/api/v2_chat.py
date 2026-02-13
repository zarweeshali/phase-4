"""
Chat API endpoint for Phase 4 Todo AI Chatbot
Stateless endpoint that persists conversation state to database
Integrates with existing authentication system
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Optional, List, Dict, Any
from backend.database.v2_connection import get_session
from backend.models.v2.models import Conversation, Message, MessageRole
from backend.agents.todo_agent import TodoAgent
from pydantic import BaseModel
from datetime import datetime
from backend.middleware.auth import get_current_user
from backend.models.user import User


router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    conversation_id: int
    response: str
    tool_calls: List[Dict[str, Any]]


@router.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Chat endpoint following the specification:
    Method: POST
    Endpoint: /api/chat (now protected by authentication)
    Description: Send message & get AI response
    
    Stateless conversation flow:
    1. Receive user message
    2. Fetch conversation history from database
    3. Build message array for agent (history + new message)
    4. Store user message in database
    5. Run agent with MCP tools
    6. Store assistant response in database
    7. Return response to client
    8. Server holds NO state (ready for next request)
    """
    
    # Use the authenticated user's ID
    user_id = str(current_user.id)  # Convert to string as required by new models
    
    # Get or create conversation
    if request.conversation_id:
        # Try to get existing conversation
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found or unauthorized")
    else:
        # Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
    
    # Store user message in database
    user_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role=MessageRole.user,
        content=request.message
    )
    session.add(user_message)
    session.commit()
    
    # Fetch conversation history from database
    statement = select(Message).where(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at)
    messages_db = session.exec(statement).all()
    
    # Convert to the format expected by the agent
    conversation_history = [
        {
            "role": msg.role.value,
            "content": msg.content
        }
        for msg in messages_db[:-1]  # Exclude the current message
    ]
    
    # Run the AI agent
    agent = TodoAgent()
    result = await agent.run(
        user_message=request.message,
        user_id=user_id,
        conversation_history=conversation_history
    )
    
    # Store assistant response in database
    assistant_message = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role=MessageRole.assistant,
        content=result["response"]
    )
    session.add(assistant_message)
    session.commit()
    
    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)
    session.commit()
    
    # Return response
    return ChatResponse(
        conversation_id=conversation.id,
        response=result["response"],
        tool_calls=result["tool_calls"]
    )