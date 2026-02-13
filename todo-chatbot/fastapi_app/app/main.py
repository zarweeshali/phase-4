from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
from app.routers import todos, chatbot
app.include_router(todos.router)
app.include_router(chatbot.router)

@app.get("/")
def read_root():
    debug_mode = os.getenv("DEBUG", "False").lower() == "true"
    return {"message": "Hello World", "debug": debug_mode}

@app.get("/chat", response_class=HTMLResponse)
async def chat_page():
    with open("app/static/index.html") as f:
        return HTMLResponse(content=f.read())