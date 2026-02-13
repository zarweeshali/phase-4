# Phase 4 Todo AI Chatbot - MCP Tools Specification

## Overview
This document specifies the MCP (Model Context Protocol) tools available to the AI agent for performing task operations in the Phase 4 Todo AI Chatbot system.

## Tool Architecture
- All tools are stateless and interact only with the database
- Tools follow the MCP protocol for standardized interaction
- Tools enforce user authorization and data isolation

## Available Tools

### 1. add_task
**Purpose**: Create a new task

**Function Signature**:
```json
{
  "name": "add_task",
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
}
```

**Example Input**:
```json
{
  "user_id": "12345",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Example Output**:
```json
{
  "task_id": 5,
  "status": "created",
  "title": "Buy groceries"
}
```

### 2. list_tasks
**Purpose**: Retrieve tasks from the list

**Function Signature**:
```json
{
  "name": "list_tasks",
  "description": "Retrieve tasks from the list",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "The user ID"},
      "status": {"type": "string", "description": "Filter tasks by status: 'all', 'pending', 'completed' (optional)"}
    },
    "required": ["user_id"]
  }
}
```

**Example Input**:
```json
{
  "user_id": "12345",
  "status": "pending"
}
```

**Example Output**:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "pending",
    "completed": false
  },
  {
    "id": 3,
    "title": "Call mom",
    "description": "Catch up on family news",
    "status": "pending",
    "completed": false
  }
]
```

### 3. complete_task
**Purpose**: Mark a task as complete

**Function Signature**:
```json
{
  "name": "complete_task",
  "description": "Mark a task as complete",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "The user ID"},
      "task_id": {"type": "integer", "description": "The ID of the task to complete"}
    },
    "required": ["user_id", "task_id"]
  }
}
```

**Example Input**:
```json
{
  "user_id": "12345",
  "task_id": 3
}
```

**Example Output**:
```json
{
  "task_id": 3,
  "status": "completed",
  "title": "Call mom"
}
```

### 4. delete_task
**Purpose**: Remove a task from the list

**Function Signature**:
```json
{
  "name": "delete_task",
  "description": "Remove a task from the list",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {"type": "string", "description": "The user ID"},
      "task_id": {"type": "integer", "description": "The ID of the task to delete"}
    },
    "required": ["user_id", "task_id"]
  }
}
```

**Example Input**:
```json
{
  "user_id": "12345",
  "task_id": 2
}
```

**Example Output**:
```json
{
  "task_id": 2,
  "status": "deleted",
  "title": "Old task"
}
```

### 5. update_task
**Purpose**: Modify task title or description

**Function Signature**:
```json
{
  "name": "update_task",
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
```

**Example Input**:
```json
{
  "user_id": "12345",
  "task_id": 1,
  "title": "Buy groceries and fruits"
}
```

**Example Output**:
```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy groceries and fruits"
}
```

## Error Handling

### Common Error Responses
All tools return error responses in the following format when an error occurs:
```json
{
  "task_id": <task_id_if_applicable>,
  "status": "error",
  "title": "<error_title>",
  "error": "<detailed_error_message>"
}
```

### Authorization Errors
- Tools validate that the user owns the task before allowing modifications
- Unauthorized attempts return an error with status "error" and appropriate message

### Validation Errors
- Tools validate input parameters before execution
- Invalid inputs return an error with status "error" and validation message

## Security Considerations
- All tools enforce user authorization by verifying user_id matches the task owner
- Tools prevent cross-user data access
- Tools sanitize inputs to prevent injection attacks