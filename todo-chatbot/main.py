"""
AI Todo AI Chatbot Backend Server
Following the constitution:
- Stateless server
- All persistent state in database
- Conversation context rebuilt per request
- MCP tools for all task operations
"""

from fastapi import FastAPI
from api.chat import router as chat_router
from database.connection import get_db
import uvicorn


app = FastAPI(
    title="AI Todo AI Chatbot API",
    description="AI-powered todo chatbot with MCP tools following Phase 4 constitution",
    version="2.0.0"
)


@app.get("/")
async def root():
    """
    Root endpoint for the AI Todo AI Chatbot
    """
    return {
        "message": "AI Todo AI Chatbot Server",
        "version": "2.0.0",
        "features": [
            "AI-powered natural language processing",
            "MCP tools for task management",
            "Stateless architecture with database persistence",
            "Authentication per Spec-4"
        ],
        "endpoints": [
            "/api/auth/signup", 
            "/api/auth/login", 
            "/api/chat"
        ]
    }


# Include the chat API router
app.include_router(chat_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)