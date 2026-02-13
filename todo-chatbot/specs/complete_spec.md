# Phase 4 Todo AI Chatbot - Complete Specification

## 1. Overview

The Phase 4 Todo AI Chatbot is an AI-powered task management system that allows users to manage their todos through natural language. The system uses OpenAI's agents framework with MCP (Model Context Protocol) tools to perform task operations.

## 2. Architecture

### 2.1 System Components
- **Frontend**: OpenAI ChatKit-inspired UI for user interaction
- **Backend**: FastAPI server with stateless endpoints
- **AI Agent**: OpenAI Agents SDK for natural language processing
- **MCP Server**: Exposes task operations as tools for the AI agent
- **Database**: SQLModel with Neon PostgreSQL for data persistence
- **Authentication**: JWT-based user management

### 2.2 Data Flow
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

## 3. Database Schema

### 3.1 Task Table
- `id`: Primary key (int, auto-increment)
- `user_id`: Owner of the task (string, indexed)
- `title`: Task title (string)
- `description`: Task description (string, optional)
- `status`: Task status (enum: pending, in_progress, completed)
- `created_at`: Creation timestamp (datetime)
- `updated_at`: Last update timestamp (datetime)

### 3.2 Conversation Table
- `id`: Primary key (int, auto-increment)
- `user_id`: Owner of the conversation (string, indexed)
- `created_at`: Creation timestamp (datetime)
- `updated_at`: Last update timestamp (datetime)

### 3.3 Message Table
- `id`: Primary key (int, auto-increment)
- `user_id`: Author of the message (string, indexed)
- `conversation_id`: Associated conversation (int, indexed)
- `role`: Message role (enum: user, assistant)
- `content`: Message content (string)
- `created_at`: Creation timestamp (datetime)

## 4. API Endpoints

### 4.1 Authentication
- `POST /api/auth/signup` - Create a new user account
- `POST /api/auth/login` - Authenticate a user

### 4.2 Chat
- `POST /api/chat` - Send a message to the AI assistant

### 4.3 Request/Response Format

#### Chat Request
```json
{
  "conversation_id": 123,  // Optional: Existing conversation ID (creates new if not provided)
  "message": "Add a task to buy groceries"  // Required: User's natural language message
}
```

#### Chat Response
```json
{
  "conversation_id": 123,  // The conversation ID
  "response": "I've added 'Buy groceries' to your task list.",  // AI assistant's response
  "tool_calls": [  // List of MCP tools invoked
    {
      "id": "call_abc123",
      "function": {
        "arguments": "{\"user_id\":\"123\",\"title\":\"Buy groceries\"}",
        "name": "add_task"
      },
      "type": "function"
    }
  ]
}
```

## 5. MCP Tools Specification

### 5.1 add_task
**Purpose**: Create a new task
**Parameters**: user_id (required), title (required), description (optional)
**Returns**: task_id, status, title

### 5.2 list_tasks
**Purpose**: Retrieve tasks from the list
**Parameters**: user_id (required), status (optional: "all", "pending", "completed")
**Returns**: Array of task objects

### 5.3 complete_task
**Purpose**: Mark a task as complete
**Parameters**: user_id (required), task_id (required)
**Returns**: task_id, status, title

### 5.4 delete_task
**Purpose**: Remove a task from the list
**Parameters**: user_id (required), task_id (required)
**Returns**: task_id, status, title

### 5.5 update_task
**Purpose**: Modify task title or description
**Parameters**: user_id (required), task_id (required), title (optional), description (optional)
**Returns**: task_id, status, title

## 6. Agent Behavior Specification

### 6.1 Task Creation
When user mentions adding/creating/remembering something, use add_task

### 6.2 Task Listing
When user asks to see/show/list tasks, use list_tasks with appropriate filter

### 6.3 Task Completion
When user says done/complete/finished, use complete_task

### 6.4 Task Deletion
When user says delete/remove/cancel, use delete_task

### 6.5 Task Update
When user says change/update/rename, use update_task

### 6.6 Confirmation
Always confirm actions with friendly response

### 6.7 Error Handling
Gracefully handle task not found and other errors

## 7. Natural Language Commands

| User Says | Agent Should |
|-----------|--------------|
| "Add a task to buy groceries" | Call add_task with title "Buy groceries" |
| "Show me all my tasks" | Call list_tasks with status "all" |
| "What's pending?" | Call list_tasks with status "pending" |
| "Mark task 3 as complete" | Call complete_task with task_id 3 |
| "Delete the meeting task" | Call list_tasks first, then delete_task |
| "Change task 1 to 'Call mom tonight'" | Call update_task with new title |
| "I need to remember to pay bills" | Call add_task with title "Pay bills" |
| "What have I completed?" | Call list_tasks with status "completed" |

## 8. Conversation Flow (Stateless Request Cycle)

1. Receive user message
2. Fetch conversation history from database
3. Build message array for agent (history + new message)
4. Store user message in database
5. Run agent with MCP tools
6. Agent invokes appropriate MCP tool(s)
7. Store assistant response in database
8. Return response to client
9. Server holds NO state (ready for next request)

## 9. Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | OpenAI ChatKit-inspired UI |
| Backend | Python FastAPI |
| AI Framework | OpenAI Agents SDK |
| MCP Server | Custom MCP Implementation |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | JWT with Better Auth concepts |

## 10. Security Considerations

- All MCP tools enforce user authorization by verifying user_id matches the task owner
- Tools prevent cross-user data access
- Tools sanitize inputs to prevent injection attacks
- JWT tokens for secure authentication
- Passwords are securely hashed

## 11. Compliance with Phase 4 Constitution

- ✅ System is fully stateless
- ✅ All persistent state lives in the database
- ✅ FastAPI server holds no memory
- ✅ Conversation context is rebuilt per request
- ✅ MCP tools are the only way to create, update, or delete tasks
- ✅ MCP tools are stateless, deterministic, and database-only
- ✅ MCP tools contain no AI logic and no memory
- ✅ Each /api/{user_id}/chat request is independent
- ✅ Conversation history is fetched from the database
- ✅ No in-process or hidden state is allowed