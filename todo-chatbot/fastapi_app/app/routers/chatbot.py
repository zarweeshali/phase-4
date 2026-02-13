from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.routers.todos import TodoItem, todos_db

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    action_taken: str = None

@router.post("/chat", response_model=ChatResponse)
def chat_with_bot(request: ChatRequest):
    """
    Simple AI chatbot that can interact with todo list
    """
    user_message = request.message.lower()
    
    # Process the user message to determine intent
    if "hello" in user_message or "hi" in user_message:
        return ChatResponse(response="Hello! I'm your AI assistant. I can help you manage your todo list. Try saying 'add a todo', 'show my todos', or 'complete a todo'.")
    
    elif "add" in user_message and "todo" in user_message:
        # Extract todo title from message (simple extraction)
        import re
        match = re.search(r"add a?n? ?todo (?:to|for|about|that|which|will)? ?(?:be )?(?:to )?(.+)", user_message)
        if match:
            title = match.group(1).strip()
            # Create a new todo
            new_todo = TodoItem(title=title, description=f"Added via chatbot: {request.message}")
            new_todo.id = len(todos_db) + 1
            todos_db.append(new_todo)
            return ChatResponse(
                response=f"I've added '{title}' to your todo list.",
                action_taken="added_todo"
            )
        else:
            return ChatResponse(response="I didn't understand what you want to add. Please say something like 'add a todo to buy groceries'.")
    
    elif "show" in user_message and "todo" in user_message:
        if not todos_db:
            return ChatResponse(response="Your todo list is empty. You can add items by saying 'add a todo to ...'")
        
        todo_titles = [f"{i+1}. {todo.title} ({'completed' if todo.completed else 'pending'})" for i, todo in enumerate(todos_db)]
        todos_str = "\n".join(todo_titles)
        return ChatResponse(
            response=f"Here are your todos:\n{todos_str}",
            action_taken="showed_todos"
        )
    
    elif "complete" in user_message and any(str(todo.id) in user_message or todo.title.lower() in user_message for todo in todos_db):
        # Find which todo to complete
        for todo in todos_db:
            if str(todo.id) in user_message or todo.title.lower() in user_message:
                todo.completed = True
                return ChatResponse(
                    response=f"I've marked '{todo.title}' as completed!",
                    action_taken="completed_todo"
                )
        return ChatResponse(response="I couldn't find that todo in your list.")
    
    elif "delete" in user_message and any(str(todo.id) in user_message or todo.title.lower() in user_message for todo in todos_db):
        # Find which todo to delete
        for i, todo in enumerate(todos_db):
            if str(todo.id) in user_message or todo.title.lower() in user_message:
                removed_title = todo.title
                del todos_db[i]
                return ChatResponse(
                    response=f"I've deleted '{removed_title}' from your todo list.",
                    action_taken="deleted_todo"
                )
        return ChatResponse(response="I couldn't find that todo in your list.")
    
    elif "help" in user_message:
        return ChatResponse(
            response="I'm your AI assistant for managing todos. You can ask me to:\n"
            "- Add a todo: 'add a todo to buy milk'\n"
            "- Show todos: 'show my todos'\n"
            "- Complete a todo: 'complete todo 1' or 'complete buy milk'\n"
            "- Delete a todo: 'delete todo 1' or 'delete buy milk'\n"
            "- Get help: 'help'"
        )
    
    else:
        return ChatResponse(
            response="I'm not sure how to help with that. Say 'help' to see what I can do, or ask me to manage your todos."
        )