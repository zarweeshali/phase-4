"""
MCP Server for Phase 4 Todo AI Chatbot
Exposes task operations as tools for the AI agent
"""

import asyncio
from typing import Dict, Any, List
from pydantic import BaseModel
from backend.mcp.v2.task_tools import (
    add_task, list_tasks, complete_task, delete_task, update_task
)
from backend.database.v2_connection import get_session


class MCPCall(BaseModel):
    """Represents an MCP call"""
    tool_name: str
    parameters: Dict[str, Any]


class MCPResult(BaseModel):
    """Represents an MCP result"""
    result: Any
    error: str = None


class MCPServer:
    """
    MCP Server that exposes tools for the AI agent
    Following the specification: MCP tools for task operations
    """
    
    def __init__(self):
        self.tools = {
            "add_task": self._execute_add_task,
            "list_tasks": self._execute_list_tasks,
            "complete_task": self._execute_complete_task,
            "delete_task": self._execute_delete_task,
            "update_task": self._execute_update_task
        }
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> MCPResult:
        """
        Execute an MCP tool with the given parameters
        """
        if tool_name not in self.tools:
            return MCPResult(error=f"Tool '{tool_name}' not found")
        
        try:
            # Get a database session
            session_gen = get_session()
            session = next(session_gen)
            
            try:
                result = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: self.tools[tool_name](session, **parameters)
                )
                return MCPResult(result=result)
            finally:
                # Close the session
                session.close()
        except Exception as e:
            return MCPResult(error=str(e))
    
    def _execute_add_task(self, session, **params):
        """Execute add_task tool"""
        return add_task(
            session=session,
            user_id=params.get("user_id"),
            title=params.get("title"),
            description=params.get("description")
        )
    
    def _execute_list_tasks(self, session, **params):
        """Execute list_tasks tool"""
        return list_tasks(
            session=session,
            user_id=params.get("user_id"),
            status=params.get("status", "all")
        )
    
    def _execute_complete_task(self, session, **params):
        """Execute complete_task tool"""
        return complete_task(
            session=session,
            user_id=params.get("user_id"),
            task_id=params.get("task_id")
        )
    
    def _execute_delete_task(self, session, **params):
        """Execute delete_task tool"""
        return delete_task(
            session=session,
            user_id=params.get("user_id"),
            task_id=params.get("task_id")
        )
    
    def _execute_update_task(self, session, **params):
        """Execute update_task tool"""
        return update_task(
            session=session,
            user_id=params.get("user_id"),
            task_id=params.get("task_id"),
            title=params.get("title"),
            description=params.get("description")
        )


# Global MCP server instance
mcp_server = MCPServer()