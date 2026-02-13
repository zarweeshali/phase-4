from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
from datetime import datetime
import uvicorn

# Initialize database
def init_db():
    conn = sqlite3.connect('simple_todo_api.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, 
                 description TEXT, status TEXT, created_at TIMESTAMP)''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

app = FastAPI(title="Todo AI Chatbot API", version="1.0.0")

class Task(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    description: Optional[str] = None
    status: str = "pending"
    created_at: Optional[str] = None

class User(BaseModel):
    id: Optional[int] = None
    username: str
    password: str

class TaskCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class MessageRequest(BaseModel):
    user_id: int
    message: str

class MessageResponse(BaseModel):
    response: str
    task_operations: List[str] = []

def get_db_connection():
    conn = sqlite3.connect('simple_todo_api.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

@app.get("/")
def read_root():
    return {"message": "Todo AI Chatbot API", "version": "1.0.0"}

@app.post("/users/", response_model=User)
def create_user(user: User):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (user.username, user.password))
        user_id = c.lastrowid
        conn.commit()
        return User(id=user_id, username=user.username, password="***")
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()

@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""INSERT INTO tasks (user_id, title, description, status, created_at) 
                 VALUES (?, ?, ?, 'pending', ?)""",
              (task.user_id, task.title, task.description, datetime.now()))
    task_id = c.lastrowid
    conn.commit()
    conn.close()
    return Task(id=task_id, user_id=task.user_id, title=task.title, 
                description=task.description, status="pending", 
                created_at=str(datetime.now()))

@app.get("/tasks/{user_id}", response_model=List[Task])
def get_tasks(user_id: int, status: Optional[str] = None):
    conn = get_db_connection()
    c = conn.cursor()
    if status:
        c.execute("SELECT * FROM tasks WHERE user_id = ? AND status = ?", (user_id, status))
    else:
        c.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [Task(id=row['id'], user_id=row['user_id'], title=row['title'], 
                 description=row['description'], status=row['status'], 
                 created_at=row['created_at']) for row in rows]

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    conn = get_db_connection()
    c = conn.cursor()
    updates = []
    params = []
    
    if task_update.title is not None:
        updates.append("title = ?")
        params.append(task_update.title)
    if task_update.description is not None:
        updates.append("description = ?")
        params.append(task_update.description)
    if task_update.status is not None:
        updates.append("status = ?")
        params.append(task_update.status)
    
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    params.append(task_id)
    query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
    c.execute(query, params)
    
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    
    conn.commit()
    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = c.fetchone()
    conn.close()
    
    return Task(id=row['id'], user_id=row['user_id'], title=row['title'], 
                description=row['description'], status=row['status'], 
                created_at=row['created_at'])

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    affected = c.rowcount
    conn.commit()
    conn.close()
    
    if affected == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task deleted successfully"}

@app.post("/chat/", response_model=MessageResponse)
def chat_with_bot(request: MessageRequest):
    user_input = request.message.lower()
    user_id = request.user_id
    task_operations = []
    
    # Simple intent recognition
    if any(word in user_input for word in ["add", "create", "new task", "remember", "note"]):
        # Extract task title
        for phrase in ["add", "create", "new task to", "remember to", "note to", "i need to"]:
            if phrase in user_input:
                title = user_input.split(phrase)[-1].strip().capitalize()
                if title:
                    conn = get_db_connection()
                    c = conn.cursor()
                    c.execute("INSERT INTO tasks (user_id, title, description, status, created_at) VALUES (?, ?, '', 'pending', ?)",
                              (user_id, title, datetime.now()))
                    task_id = c.lastrowid
                    conn.commit()
                    conn.close()
                    response = f"I've added '{title}' to your task list (Task #{task_id})."
                    task_operations.append(f"Added task: {title}")
                    return MessageResponse(response=response, task_operations=task_operations)
        
        title = user_input.replace("add", "").replace("create", "").replace("new task", "").strip().capitalize()
        if title:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO tasks (user_id, title, description, status, created_at) VALUES (?, ?, '', 'pending', ?)",
                      (user_id, title, datetime.now()))
            task_id = c.lastrowid
            conn.commit()
            conn.close()
            response = f"I've added '{title}' to your task list (Task #{task_id})."
            task_operations.append(f"Added task: {title}")
        else:
            response = "What task would you like to add?"
        
        return MessageResponse(response=response, task_operations=task_operations)
    
    elif any(word in user_input for word in ["show", "list", "see", "view", "display", "my tasks", "what"]):
        status = "all"
        if "pending" in user_input or "incomplete" in user_input:
            status = "pending"
        elif "completed" in user_input or "done" in user_input:
            status = "completed"
        
        conn = get_db_connection()
        c = conn.cursor()
        if status == "all":
            c.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
        else:
            c.execute("SELECT * FROM tasks WHERE user_id = ? AND status = ?", (user_id, status))
        tasks = c.fetchall()
        conn.close()
        
        if not tasks:
            if status == "all":
                response = "You don't have any tasks."
            else:
                response = f"You don't have any {status} tasks."
        else:
            task_list = "\n".join([f"- {task['title']} (ID: {task['id']}, Status: {task['status']})" for task in tasks])
            response = f"Your {status} tasks:\n{task_list}"
        
        task_operations.append(f"Retrieved {status} tasks for user {user_id}")
        return MessageResponse(response=response, task_operations=task_operations)
    
    elif any(word in user_input for word in ["complete", "done", "finish", "mark as done"]):
        import re
        numbers = re.findall(r'\d+', user_input)
        if numbers:
            task_id = int(numbers[0])
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("UPDATE tasks SET status = 'completed' WHERE id = ? AND user_id = ?", (task_id, user_id))
            if c.rowcount > 0:
                conn.commit()
                response = f"I've marked task #{task_id} as completed."
                task_operations.append(f"Completed task #{task_id}")
            else:
                response = f"Task #{task_id} not found in your task list."
            conn.close()
        else:
            response = "Which task would you like to mark as complete? Please specify the task number."
        
        return MessageResponse(response=response, task_operations=task_operations)
    
    elif any(word in user_input for word in ["delete", "remove", "cancel", "eliminate"]):
        import re
        numbers = re.findall(r'\d+', user_input)
        if numbers:
            task_id = int(numbers[0])
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
            if c.rowcount > 0:
                conn.commit()
                response = f"I've deleted task #{task_id}."
                task_operations.append(f"Deleted task #{task_id}")
            else:
                response = f"Task #{task_id} not found in your task list."
            conn.close()
        else:
            response = "Which task would you like to delete? Please specify the task number."
        
        return MessageResponse(response=response, task_operations=task_operations)
    
    else:
        response = f"I received your message: '{request.message}'. I can help you manage tasks. Try commands like: 'Add a task to buy groceries', 'Show my tasks', 'Mark task 1 as complete', or 'Delete task 1'."
        return MessageResponse(response=response, task_operations=task_operations)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)