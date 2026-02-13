# Todo AI Chatbot

This is a FastAPI-based application that combines a todo list manager with an AI chatbot interface.

## Features

- **Todo Management**: Add, view, update, and delete todo items
- **AI Chat Interface**: Natural language interaction to manage your todos
- **Web Interface**: Simple HTML/JS frontend to interact with the chatbot

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone or copy the project files
2. Navigate to the project directory: `cd fastapi_app`
3. Install dependencies: `pip install -r requirements.txt`

### Running the Application

1. Run the server: `uvicorn app.main:app --reload`
2. Access the API documentation at: `http://localhost:8000/docs`
3. Access the chatbot interface at: `http://localhost:8000/chat`

## Chatbot Commands

The AI chatbot understands the following commands:

- `"add a todo to buy groceries"` - Adds a new todo item
- `"show my todos"` - Lists all your todo items
- `"complete todo 1"` or `"complete buy groceries"` - Marks a todo as completed
- `"delete todo 1"` or `"delete buy groceries"` - Removes a todo from the list
- `"help"` - Shows available commands

## API Endpoints

- `GET /` - Root endpoint
- `GET /chat` - Chatbot web interface
- `POST /chatbot/chat` - Chat with the AI assistant
- `GET /todos/` - Get all todos
- `POST /todos/` - Create a new todo
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a specific todo
- `DELETE /todos/{id}` - Delete a specific todo

## Architecture

- `app/main.py` - Main application with routing
- `app/routers/todos.py` - Todo management endpoints
- `app/routers/chatbot.py` - AI chatbot endpoints
- `app/static/index.html` - Frontend interface
- `.env` - Environment variables

## Environment Variables

The application supports the following environment variables:

- `DEBUG` - Enable/disable debug mode (default: False)
- `DATABASE_URL` - Database connection string (default: SQLite)
- `SECRET_KEY` - Secret key for security
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time

## Future Enhancements

- Integration with actual AI services (OpenAI, etc.) for more sophisticated responses
- Database persistence (PostgreSQL, MongoDB, etc.)
- User authentication and authorization
- More advanced natural language processing
- Voice input/output capabilities