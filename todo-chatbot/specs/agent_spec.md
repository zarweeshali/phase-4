# Phase 4 Todo AI Chatbot - Agent Specification

## Overview
This document specifies the behavior and capabilities of the AI agent in the Phase 4 Todo AI Chatbot system.

## Agent Purpose
The AI agent serves as a natural language interface for managing todo tasks. It interprets user requests and executes appropriate MCP tools to manage tasks in the database.

## Agent Capabilities

### 1. Task Creation
- **Trigger**: When user mentions adding/creating/remembering something
- **Action**: Use `add_task` MCP tool
- **Examples**:
  - "Add a task to buy groceries"
  - "Create a reminder to call mom"
  - "I need to remember to pay bills"

### 2. Task Listing
- **Trigger**: When user asks to see/show/list tasks
- **Action**: Use `list_tasks` MCP tool with appropriate filter
- **Examples**:
  - "Show me all my tasks"
  - "What's pending?"
  - "What have I completed?"
  - "List my tasks"

### 3. Task Completion
- **Trigger**: When user says done/complete/finished
- **Action**: Use `complete_task` MCP tool
- **Examples**:
  - "Mark task 3 as complete"
  - "I finished the report"
  - "Complete task 'buy groceries'"

### 4. Task Deletion
- **Trigger**: When user says delete/remove/cancel
- **Action**: Use `delete_task` MCP tool
- **Examples**:
  - "Delete the meeting task"
  - "Remove task 2"
  - "Cancel 'pick up kids' task"

### 5. Task Update
- **Trigger**: When user says change/update/rename
- **Action**: Use `update_task` MCP tool
- **Examples**:
  - "Change task 1 to 'Call mom tonight'"
  - "Update the grocery list task"
  - "Rename 'work thing' to 'finish presentation'"

## Response Guidelines

### Confirmation
- Always confirm actions with friendly response
- Example: "I've added 'Buy groceries' to your task list."

### Error Handling
- Gracefully handle task not found and other errors
- Provide helpful error messages to the user
- Example: "I couldn't find a task with ID 5. Please check the task number."

### Clarification
- Ask for clarification when user intent is ambiguous
- Example: "Which task would you like to mark as complete? I found multiple tasks matching 'groceries'."

## Natural Language Understanding

The agent should understand various ways users express their intent:

### Task Creation Phrases
- Add, create, make, remember, note, jot down, put in my list
- Examples: "Add buy milk", "Create a task to call John", "Remember to water plants"

### Task Listing Phrases
- Show, list, display, see, view, get, fetch, tell me
- Examples: "Show my tasks", "What do I have to do?", "List everything"

### Task Completion Phrases
- Complete, finish, done, mark as done, check off, tick
- Examples: "I'm done with task 3", "Complete the laundry", "Finish 'call dentist'"

### Task Deletion Phrases
- Delete, remove, eliminate, get rid of, cancel, scratch off
- Examples: "Delete task 1", "Remove 'buy bread'", "Cancel this task"

### Task Update Phrases
- Change, update, modify, edit, rename, alter
- Examples: "Change 'buy food' to 'buy groceries'", "Update the due date"

## Context Awareness
- Maintain awareness of recent conversation context
- Reference previously mentioned tasks by name or position
- Handle follow-up questions appropriately