"""
Mock AI Agent for Phase 4 Todo AI Chatbot
This implementation works without an API key and simulates AI behavior
"""

import asyncio
from typing import Dict, Any, List
import re
from backend.mcp.v2.server import mcp_server
import os


class TodoAgent:
    """
    AI Agent for managing todos through natural language
    Uses MCP tools to perform task operations
    """
    
    def __init__(self):
        # Check if API key is available
        self.has_api_key = bool(os.getenv("GOOGLE_API_KEY"))
        print(f"API Key Status: {'Available' if self.has_api_key else 'Not available - using mock responses'}")
        
        # Define the tools available to the agent
        self.tools_info = {
            "add_task": {
                "description": "Create a new task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "title": {"type": "string", "description": "The task title"},
                        "description": {"type": "string", "description": "The task description (optional)"}
                    },
                    "required": ["user_id", "title"]
                }
            },
            "list_tasks": {
                "description": "Retrieve tasks from the list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "status": {"type": "string", "description": "Filter tasks by status: 'all', 'pending', 'completed' (optional)"}
                    },
                    "required": ["user_id"]
                }
            },
            "complete_task": {
                "description": "Mark a task as complete",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            "delete_task": {
                "description": "Remove a task from the list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            "update_task": {
                "description": "Modify task title or description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "task_id": {"type": "integer", "description": "The ID of the task to update"},
                        "title": {"type": "string", "description": "The new task title (optional)"},
                        "description": {"type": "string", "description": "The new task description (optional)"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        }
    
    async def run(self, user_message: str, user_id: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Run the agent with the given user message and conversation history
        """
        # Simple keyword-based detection for task operations
        user_msg_lower = user_message.lower()
        
        # Detect intent based on keywords
        if any(keyword in user_msg_lower for keyword in ["add", "create", "new task", "remember", "note", "schedule"]):
            # Extract potential task title from the message
            # Remove common phrases to isolate the task
            task_text = user_msg_lower
            for phrase in ["add", "create", "new task to", "remember to", "note to", "i need to", "i have to"]:
                task_text = task_text.replace(phrase, "").strip()
            
            # Use the remaining text as the task title
            title = task_text.capitalize() if task_text else "New Task"
            
            # Execute add_task
            params = {"user_id": user_id, "title": title}
            result = await mcp_server.execute_tool("add_task", params)
            
            if result.error:
                response = f"Sorry, I couldn't add the task: {result.error}"
            else:
                response = f"I've added '{title}' to your task list."
            
            return {
                "response": response,
                "tool_calls": [{
                    "name": "add_task",
                    "arguments": str(params)
                }]
            }
        
        elif any(keyword in user_msg_lower for keyword in ["show", "list", "see", "view", "display", "my tasks", "what"]):
            # Determine status to filter by
            status = "all"
            if "pending" in user_msg_lower or "incomplete" in user_msg_lower:
                status = "pending"
            elif "completed" in user_msg_lower or "done" in user_msg_lower:
                status = "completed"
            
            params = {"user_id": user_id, "status": status}
            result = await mcp_server.execute_tool("list_tasks", params)
            
            if result.error:
                response = f"Sorry, I couldn't retrieve your tasks: {result.error}"
            else:
                tasks = result.result
                if not tasks:
                    if status == "all":
                        response = "You don't have any tasks."
                    else:
                        response = f"You don't have any {status} tasks."
                else:
                    task_list = ", ".join([f"'{task['title']}'" for task in tasks[:5]])  # Limit to first 5
                    if len(tasks) > 5:
                        task_list += f" and {len(tasks)-5} more"
                    response = f"Your {status} tasks are: {task_list}."
            
            return {
                "response": response,
                "tool_calls": [{
                    "name": "list_tasks",
                    "arguments": str(params)
                }]
            }
        
        elif any(keyword in user_msg_lower for keyword in ["complete", "done", "finish", "mark as done"]):
            # Try to extract task ID from the message
            task_id = None
            # Look for numbers in the message that might represent task IDs
            numbers = re.findall(r'\d+', user_msg_lower)
            if numbers:
                try:
                    task_id = int(numbers[0])
                except ValueError:
                    pass
            
            if task_id is not None:
                params = {"user_id": user_id, "task_id": task_id}
                result = await mcp_server.execute_tool("complete_task", params)
                
                if result.error:
                    response = f"Sorry, I couldn't complete the task: {result.error}"
                else:
                    response = f"I've marked task #{task_id} as completed."
                
                return {
                    "response": response,
                    "tool_calls": [{
                        "name": "complete_task",
                        "arguments": str(params)
                    }]
                }
            else:
                # If no specific task ID found, suggest listing tasks first
                return {
                    "response": "Which task would you like to mark as complete? Please specify the task number or list your tasks first.",
                    "tool_calls": []
                }
        
        elif any(keyword in user_msg_lower for keyword in ["delete", "remove", "cancel", "eliminate"]):
            # Try to extract task ID from the message
            task_id = None
            # Look for numbers in the message that might represent task IDs
            numbers = re.findall(r'\d+', user_msg_lower)
            if numbers:
                try:
                    task_id = int(numbers[0])
                except ValueError:
                    pass
            
            if task_id is not None:
                params = {"user_id": user_id, "task_id": task_id}
                result = await mcp_server.execute_tool("delete_task", params)
                
                if result.error:
                    response = f"Sorry, I couldn't delete the task: {result.error}"
                else:
                    response = f"I've deleted task #{task_id}."
                
                return {
                    "response": response,
                    "tool_calls": [{
                        "name": "delete_task",
                        "arguments": str(params)
                    }]
                }
            else:
                # If no specific task ID found, suggest listing tasks first
                return {
                    "response": "Which task would you like to delete? Please specify the task number or list your tasks first.",
                    "tool_calls": []
                }
        
        elif any(keyword in user_msg_lower for keyword in ["update", "change", "modify", "edit", "rename"]):
            # This is more complex, so we'll just respond with instructions
            return {
                "response": "To update a task, please specify which task by number and what changes you'd like to make.",
                "tool_calls": []
            }
        
        else:
            # Default response for unrecognized commands
            return {
                "response": f"I understand you said: '{user_message}'. I can help you manage tasks by adding, listing, completing, or deleting them. Try saying something like 'Add a task to buy groceries' or 'Show me my tasks'.",
                "tool_calls": []
            }