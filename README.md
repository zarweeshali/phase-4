# Phase 4 Todo AI Chatbot

This project implements an AI-powered todo chatbot following the Phase 4 architecture and specifications.

## Overview

The Phase 4 Todo AI Chatbot is a natural language task management system that allows users to manage their todos through conversational AI. The system uses Google's Gemini AI with MCP (Model Context Protocol) tools to perform task operations.

## Features

- Natural language processing for task management
- AI-powered conversation interface
- MCP tools for task operations (add, list, complete, delete, update)
- Stateless architecture with database persistence
- User authentication and authorization
- Conversation history management

## Docker Images

Two Docker images are provided for easy deployment:

### Backend Image
- **Image Name**: `todo-backend`
- **Purpose**: Contains the FastAPI server, AI integration, and MCP tools
- **Port**: 8000
- **Function**: Handles API requests, AI processing, and database operations

### Frontend Image  
- **Image Name**: `todo-frontend`
- **Purpose**: Contains the Streamlit-based user interface
- **Port**: 8501
- **Function**: Provides the chat interface for users

## Running the Application

### Prerequisites
- Docker and Docker Compose
- Google Gemini API key (for full AI functionality)

### Quick Start

1. **Run the backend service:**
   ```bash
   docker run -d -p 8000:8000 --name todo-backend-container todo-backend
   ```

2. **Run the frontend service:**
   ```bash
   docker run -d -p 8501:8501 --name todo-frontend-container todo-frontend
   ```

3. **Access the application:**
   - Backend API: http://localhost:8000
   - Frontend UI: http://localhost:8501

### With Docker Network (Recommended for inter-service communication)

1. **Create a network:**
   ```bash
   docker network create todo-network
   ```

2. **Run backend service:**
   ```bash
   docker run -d -p 8000:8000 --network todo-network --name todo-backend-service todo-backend
   ```

3. **Run frontend service:**
   ```bash
   docker run -d -p 8501:8501 --network todo-network --name todo-frontend-service todo-frontend
   ```

## Architecture

The system follows a microservice architecture with clear separation of concerns:

### Backend Components
- **FastAPI Server**: Main application server with stateless endpoints
- **Google Gemini AI**: AI logic for natural language processing
- **MCP Server**: Exposes task operations as tools for the AI agent
- **SQLModel ORM**: Database abstraction layer
- **Neon PostgreSQL**: Production-ready database backend
- **Authentication**: Secure user management with JWT tokens

### Frontend Components
- **Streamlit UI**: Modern chat interface
- **Authentication Flow**: Secure login/signup process
- **Real-time Messaging**: Interactive chat experience

## Configuration

### Environment Variables

For full functionality, set these environment variables:

**Backend:**
- `GOOGLE_API_KEY`: Your Google Gemini API key
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT tokens

**Frontend:**
- `BACKEND_URL`: URL of the backend service (when deployed separately)

## MCP Tools

The system implements the following MCP tools for the AI agent:

- `add_task`: Create a new task
- `list_tasks`: Retrieve tasks with optional filtering
- `complete_task`: Mark a task as complete
- `delete_task`: Remove a task
- `update_task`: Modify task properties

## Natural Language Commands

The chatbot understands various natural language commands:

| User Says | System Action |
|-----------|---------------|
| "Add a task to buy groceries" | Creates a new task titled "buy groceries" |
| "Show me all my tasks" | Lists all tasks |
| "What's pending?" | Lists pending tasks |
| "Mark task 3 as complete" | Marks task with ID 3 as complete |
| "Delete the meeting task" | Deletes the specified task |
| "Change task 1 to 'Call mom tonight'" | Updates task 1's title |

## Phase 4 Constitution Compliance

The system follows the Phase 4 constitution:

- ✅ System is fully stateless
- ✅ All persistent state lives in the database
- ✅ FastAPI server holds no memory
- ✅ MCP tools are the only way to create, update, or delete data
- ✅ Tools sanitize inputs to prevent injection attacks
- ✅ JWT tokens for secure authentication
- ✅ Passwords are securely hashed

## Database Schema

### Task Table
- `id`: Primary key
- `user_id`: Owner of the task (string)
- `title`: Task title
- `description`: Task description (optional)
- `status`: Task status (pending, in_progress, completed)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Conversation Table
- `id`: Primary key
- `user_id`: Owner of the conversation (string)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Message Table
- `id`: Primary key
- `user_id`: Author of the message (string)
- `conversation_id`: Associated conversation
- `role`: Message role (user, assistant)
- `content`: Message content
- `created_at`: Creation timestamp