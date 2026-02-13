import streamlit as st
import json
import sqlite3
from datetime import datetime
import os

# Set page config
st.set_page_config(page_title="Simple Todo AI Chatbot", layout="centered")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Database setup
def init_db():
    conn = sqlite3.connect('simple_todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, 
                 description TEXT, status TEXT, created_at TIMESTAMP)''')
    conn.commit()
    conn.close()

def add_task(user_id, title, description=""):
    conn = sqlite3.connect('simple_todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (user_id, title, description, status, created_at) VALUES (?, ?, ?, 'pending', ?)",
              (user_id, title, description, datetime.now()))
    conn.commit()
    task_id = c.lastrowid
    conn.close()
    return task_id

def get_tasks(user_id, status="all"):
    conn = sqlite3.connect('simple_todo.db')
    c = conn.cursor()
    if status == "all":
        c.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
    else:
        c.execute("SELECT * FROM tasks WHERE user_id = ? AND status = ?", (user_id, status))
    tasks = c.fetchall()
    conn.close()
    return tasks

def complete_task(task_id):
    conn = sqlite3.connect('simple_todo.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('simple_todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Simple AI logic
def simple_ai_response(user_input, user_id):
    user_input_lower = user_input.lower()
    
    # Add task
    if any(word in user_input_lower for word in ["add", "create", "new task", "remember", "note"]):
        # Extract task title (simple approach)
        for phrase in ["add", "create", "new task to", "remember to", "note to", "i need to"]:
            if phrase in user_input_lower:
                title = user_input_lower.split(phrase)[-1].strip().capitalize()
                if title:
                    task_id = add_task(user_id, title)
                    return f"I've added '{title}' to your task list (Task #{task_id})."
        
        # If no specific phrase matched, use the whole input minus command words
        title = user_input_lower.replace("add", "").replace("create", "").replace("new task", "").strip().capitalize()
        if title:
            task_id = add_task(user_id, title)
            return f"I've added '{title}' to your task list (Task #{task_id})."
        else:
            return "What task would you like to add?"
    
    # List tasks
    elif any(word in user_input_lower for word in ["show", "list", "see", "view", "my tasks", "what"]):
        status = "all"
        if "pending" in user_input_lower or "incomplete" in user_input_lower:
            status = "pending"
        elif "completed" in user_input_lower or "done" in user_input_lower:
            status = "completed"
        
        tasks = get_tasks(user_id, status)
        
        if not tasks:
            if status == "all":
                return "You don't have any tasks."
            else:
                return f"You don't have any {status} tasks."
        else:
            task_list = "\n".join([f"- {task[2]} (ID: {task[0]}, Status: {task[4]})" for task in tasks])
            return f"Your {status} tasks:\n{task_list}"
    
    # Complete task
    elif any(word in user_input_lower for word in ["complete", "done", "finish", "mark as done"]):
        # Try to extract task ID
        import re
        numbers = re.findall(r'\d+', user_input_lower)
        if numbers:
            task_id = int(numbers[0])
            # Verify task belongs to user
            user_tasks = [t[0] for t in get_tasks(user_id)]
            if task_id in user_tasks:
                complete_task(task_id)
                return f"I've marked task #{task_id} as completed."
            else:
                return f"Task #{task_id} not found in your task list."
        else:
            return "Which task would you like to mark as complete? Please specify the task number."
    
    # Delete task
    elif any(word in user_input_lower for word in ["delete", "remove", "cancel", "eliminate"]):
        # Try to extract task ID
        import re
        numbers = re.findall(r'\d+', user_input_lower)
        if numbers:
            task_id = int(numbers[0])
            # Verify task belongs to user
            user_tasks = [t[0] for t in get_tasks(user_id)]
            if task_id in user_tasks:
                delete_task(task_id)
                return f"I've deleted task #{task_id}."
            else:
                return f"Task #{task_id} not found in your task list."
        else:
            return "Which task would you like to delete? Please specify the task number."
    
    # Default response
    else:
        return f"I received your message: '{user_input}'. I can help you manage tasks. Try commands like: 'Add a task to buy groceries', 'Show my tasks', 'Mark task 1 as complete', or 'Delete task 1'."

# Main app
st.title("🤖 Simple Todo AI Chatbot")
st.caption("A basic but functional todo manager with AI-like responses")

# Simple login
if not st.session_state.logged_in:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login / Sign Up")
        
        if submitted and username and password:
            conn = sqlite3.connect('simple_todo.db')
            c = conn.cursor()
            try:
                # Try to create user (will fail if exists)
                c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", (username, password))
                # Then try to authenticate
                c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
                user = c.fetchone()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            finally:
                conn.close()
else:
    # Show user info
    st.sidebar.success(f"Logged in as User ID: {st.session_state.user_id}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.messages = []
        st.rerun()
    
    # Chat interface
    # Display messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # Input for new message
    if prompt := st.chat_input("Type a command (e.g., 'Add a task to buy groceries')..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                response = simple_ai_response(prompt, st.session_state.user_id)
                st.write(response)
        
        # Add AI response to history
        st.session_state.messages.append({"role": "assistant", "content": response})