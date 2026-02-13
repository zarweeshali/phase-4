# Phase 4 Constitution

## Core Rules

- The system is fully stateless
- All persistent state lives in the database
- The FastAPI server holds no memory
- Conversation context is rebuilt per request

## MCP Rules

- MCP tools are the only way to create, update, or delete tasks
- MCP tools are:
  - Stateless
  - Deterministic
  - Database-only
- MCP tools contain no AI logic and no memory

## Agent Rules

- The AI agent must always use MCP tools for task operations
- The agent must not guess task identity
- The agent must confirm all successful actions
- The agent must handle errors gracefully
- The agent never accesses the database directly

## Conversation Contract

- Each `/api/{user_id}/chat` request is independent
- Conversation history is fetched from the database
- No in-process or hidden state is allowed

## Feature Expansion

New features must:

- Reuse the same agent and MCP server
- Preserve stateless architecture
- Be additive and backward-compatible

## Compliance

Any implementation that:

- Bypasses MCP
- Stores in-memory state
- Modifies data without tools

is non-compliant with Phase 4.