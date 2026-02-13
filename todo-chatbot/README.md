# Phase 4 Todo AI Chatbot

This project implements an AI-powered todo chatbot following the Phase 4 architecture and specifications:

## Overview

The Phase 4 Todo AI Chatbot is a natural language task management system that allows users to manage their todos through conversational AI. The system uses Google's Gemini AI with MCP (Model Context Protocol) tools to perform task operations.

## Core Features

- Natural language processing for task management
- AI-powered conversation interface
- MCP tools for task operations (add, list, complete, delete, update)
- Stateless architecture with database persistence
- User authentication and authorization
- Conversation history management

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
- **OpenAI ChatKit-inspired UI**: Modern chat interface
- **Authentication Flow**: Secure login/signup process
- **Real-time Messaging**: Interactive chat experience

### Data Flow
```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │              FastAPI Server                   │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │    Neon DB      │
│  Chat Interface │────▶│  │         Chat Endpoint                  │  │     │  (PostgreSQL)   │
│  (Frontend)     │     │  │  POST /api/chat                        │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │  - tasks        │
│                 │     │                  │                           │     │  - conversations│
│                 │     │                  ▼                           │     │  - messages     │
│                 │◀────│  ┌────────────────────────────────────────┐  │     │                 │
│                 │     │  │      OpenAI Agents SDK                 │  │     │                 │
│                 │     │  │      (Agent + Runner)                  │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │                 │
│                 │     │                  ▼                           │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │────▶│                 │
│                 │     │  │         MCP Server                     │  │     │                 │
│                 │     │  │  (MCP Tools for Task Operations)       │  │◀────│                 │
│                 │     │  └────────────────────────────────────────┘  │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

## Getting Started

### Prerequisites
- Python 3.8+
- Google Gemini API key
- (For production) Neon PostgreSQL account

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd phase-4
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export OPENAI_API_KEY='your-openai-api-key'
export DATABASE_URL='postgresql://username:password@neon-host/dbname'
```

4. Initialize the database:
```bash
python backend/init_v2_db.py
```

5. Run the backend server:
```bash
cd backend
uvicorn main:app --reload
```

6. Serve the frontend:
```bash
cd frontend
python -m http.server 3000
```

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
DATABASE_URL=postgresql://username:password@host:port/database_name
SECRET_KEY=your_secret_key_for_jwt_tokens
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create a new user account
- `POST /api/auth/login` - Authenticate a user

### Chat
- `POST /api/chat` - Send a message to the AI assistant

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

## MCP Tools

The system implements the following MCP tools for the AI agent:

- `add_task`: Create a new task
- `list_tasks`: Retrieve tasks with optional filtering
- `complete_task`: Mark a task as complete
- `delete_task`: Remove a task
- `update_task`: Modify task properties

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.