import streamlit as st
import requests
import json
from datetime import datetime

# Set page config
st.set_page_config(page_title="AI Todo AI Chatbot", layout="wide")

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'current_conversation_id' not in st.session_state:
    st.session_state.current_conversation_id = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Backend URL
BACKEND_URL = "http://localhost:8001"

def signup(email, password):
    """Sign up a new user"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/auth/signup",
            json={"email": email, "password": password}
        )
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"detail": str(e)}, False

def login(email, password):
    """Log in a user"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/auth/login",
            json={"email": email, "password": password}
        )
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"detail": str(e)}, False

def send_message(message):
    """Send a message to the AI assistant"""
    if not st.session_state.token:
        st.error("Please log in first")
        return None
    
    try:
        headers = {
            "Authorization": f"Bearer {st.session_state.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "conversation_id": st.session_state.current_conversation_id,
            "message": message
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            # Update conversation ID if it's the first message
            if not st.session_state.current_conversation_id:
                st.session_state.current_conversation_id = data["conversation_id"]
            return data
        else:
            st.error(f"Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error sending message: {str(e)}")
        return None

# Main app
st.title("🤖 AI Todo AI Chatbot")
st.markdown("*Natural Language Task Management*")

# Authentication section
if not st.session_state.token:
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            data, success = login(login_email, login_password)
            if success:
                st.session_state.token = data["access_token"]
                st.session_state.user_email = data["email"]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(f"Login failed: {data.get('detail', 'Unknown error')}")
    
    with tab2:
        st.subheader("Sign Up")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        
        if st.button("Sign Up"):
            data, success = signup(signup_email, signup_password)
            if success:
                st.success("Account created successfully! Please log in.")
            else:
                st.error(f"Sign up failed: {data.get('detail', 'Unknown error')}")
else:
    # User is logged in
    st.sidebar.success(f"Logged in as: {st.session_state.user_email}")
    
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user_email = None
        st.session_state.current_conversation_id = None
        st.session_state.messages = []
        st.rerun()
    
    # Chat interface
    st.subheader("Chat with Your AI Assistant")
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input for new message
    if prompt := st.chat_input("Ask me to manage your tasks..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message(prompt)
                
            if response:
                assistant_response = response["response"]
                st.write(assistant_response)
                
                # Add assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                
                # Show tool calls if any
                if response.get("tool_calls"):
                    with st.expander("Tool Calls Executed"):
                        st.json(response["tool_calls"])
            else:
                st.error("Failed to get response from AI assistant")