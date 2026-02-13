import streamlit as st
import requests
import json
from datetime import datetime

# Set up the page
st.set_page_config(page_title="Todo AI Chatbot", layout="wide")
st.title("🤖 Todo AI Chatbot")
st.markdown("I'm your AI assistant for managing todos. Ask me to add, complete, or show your tasks!")

# Initialize session state for chat history and todos
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'todos' not in st.session_state:
    st.session_state.todos = []

# Function to simulate the AI chatbot response
def get_chatbot_response(user_message):
    # This is a simplified version - in a real app, this would connect to your FastAPI backend
    user_message_lower = user_message.lower().strip()
    
    # Handle greetings
    if any(greeting in user_message_lower for greeting in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        return "Hello! I'm your AI assistant. I can help you manage your todo list. Try saying 'add a todo', 'show my todos', or 'complete a todo'."
    
    # Handle yes/no responses
    if user_message_lower in ["yes", "yeah", "yep", "sure", "ok", "okay"]:
        return "Great! What would you like to do? You can ask me to add, show, complete, or delete todos."
    
    if user_message_lower in ["no", "nope", "nah"]:
        return "No problem! Let me know if there's anything I can help you with."
    
    # Handle adding todos
    if any(add_word in user_message_lower for add_word in ["add", "create", "make", "new"]) and "todo" in user_message_lower:
        # Extract todo title from message (simple extraction)
        import re
        match = re.search(r"(?:add|create|make|new)\s+a?\s*todo?\s+(?:to|for|about|that|which|will)?\s*(?:be\s*)?(?:to\s*)?(.+)", user_message_lower)
        if match:
            title = match.group(1).strip().capitalize()
            # Add to session state
            new_todo = {
                "id": len(st.session_state.todos) + 1,
                "title": title,
                "description": f"Added via chatbot: {user_message}",
                "completed": False,
                "created_at": datetime.now().isoformat()
            }
            st.session_state.todos.append(new_todo)
            return f"I've added '{title}' to your todo list!"
        else:
            return "I didn't understand what you want to add. Please say something like 'add a todo to buy groceries'."
    
    # Handle showing todos
    elif any(show_word in user_message_lower for show_word in ["show", "display", "list", "see", "view"]) and any(todo_word in user_message_lower for todo_word in ["todo", "todos", "task", "tasks"]):
        if not st.session_state.todos:
            return "Your todo list is empty. You can add items by saying 'add a todo to ...'"
        
        todo_titles = [f"{i+1}. {todo['title']} ({'completed' if todo['completed'] else 'pending'})" for i, todo in enumerate(st.session_state.todos)]
        todos_str = "\n".join(todo_titles)
        return f"Here are your todos:\n{todos_str}"
    
    # Handle completing todos
    elif any(comp_word in user_message_lower for comp_word in ["complete", "finish", "done", "completed", "mark as done"]):
        # Find which todo to complete
        for todo in st.session_state.todos:
            if str(todo['id']) in user_message_lower or todo['title'].lower() in user_message_lower:
                todo['completed'] = True
                return f"I've marked '{todo['title']}' as completed!"
        return "I couldn't find that todo in your list."
    
    # Handle deleting todos
    elif any(del_word in user_message_lower for del_word in ["delete", "remove", "erase", "cancel"]):
        # Find which todo to delete
        for i, todo in enumerate(st.session_state.todos):
            if str(todo['id']) in user_message_lower or todo['title'].lower() in user_message_lower:
                removed_title = todo['title']
                del st.session_state.todos[i]
                return f"I've deleted '{removed_title}' from your todo list."
        return "I couldn't find that todo in your list."
    
    # Handle help requests
    elif "help" in user_message_lower or "what can you do" in user_message_lower:
        return (
            "I'm your AI assistant for managing todos. You can ask me to:\n"
            "- Add a todo: 'add a todo to buy milk'\n"
            "- Show todos: 'show my todos'\n"
            "- Complete a todo: 'complete todo 1' or 'complete buy milk'\n"
            "- Delete a todo: 'delete todo 1' or 'delete buy milk'\n"
            "- Get help: 'help'"
        )
    
    # Default response
    else:
        return "I'm not sure how to help with that. Say 'help' to see what I can do, or ask me to manage your todos."

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    # Chat interface
    st.subheader("💬 Chat with AI Assistant")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Bot:** {message['content']}")
    
    # Input for new message
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("Type your message here...")
        submit_button = st.form_submit_button(label='Send')
        
        if submit_button and user_input.strip():
            # Add user message to history
            st.session_state.chat_history.append({'role': 'user', 'content': user_input})
            
            # Get and add bot response to history
            bot_response = get_chatbot_response(user_input)
            st.session_state.chat_history.append({'role': 'bot', 'content': bot_response})
            
            # Rerun to update the chat display
            st.rerun()

with col2:
    # Todo list display
    st.subheader("📋 Your Todo List")
    
    if st.session_state.todos:
        for i, todo in enumerate(st.session_state.todos):
            # Create a container for each todo item
            with st.container():
                # Checkbox for completion status
                completed = st.checkbox(
                    label=f"{todo['title']}", 
                    value=todo['completed'], 
                    key=f"todo_{i}_{todo['id']}"
                )
                
                # Update the todo's completion status
                st.session_state.todos[i]['completed'] = completed
                
                # Show description if available
                if todo['description']:
                    st.caption(todo['description'])
                
                # Divider between todos
                st.divider()
    else:
        st.info("Your todo list is empty. Add items using the chat!")

# Add some instructions at the bottom
st.markdown("---")
st.markdown("### How to use:")
st.markdown("- Type messages in the chat to interact with the AI assistant")
st.markdown("- The assistant can add, show, complete, and delete todos")
st.markdown("- Your todos appear in the right panel")