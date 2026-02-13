from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/todos", tags=["todos"])

# Data model for todos
class TodoItem(BaseModel):
    id: Optional[int] = None
    title: str
    description: str = ""
    completed: bool = False

# In-memory storage for todos (in production, you'd use a database)
todos_db = []
next_id = 1

@router.get("/", response_model=List[TodoItem])
def get_todos(completed: Optional[bool] = Query(None)):
    """Get all todos, optionally filtered by completion status"""
    if completed is None:
        return todos_db
    return [todo for todo in todos_db if todo.completed == completed]

@router.post("/", response_model=TodoItem)
def create_todo(todo: TodoItem):
    """Create a new todo item"""
    global next_id
    todo.id = next_id
    next_id += 1
    todos_db.append(todo)
    return todo

@router.get("/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.put("/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    """Update a specific todo by ID"""
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            todos_db[i] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/{todo_id}")
def delete_todo(todo_id: int):
    """Delete a specific todo by ID"""
    global todos_db
    initial_length = len(todos_db)
    todos_db = [todo for todo in todos_db if todo.id != todo_id]
    
    if len(todos_db) == initial_length:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return {"message": "Todo deleted successfully"}