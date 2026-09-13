from uuid import uuid4

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from main import run_agent

import os




# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="AI Expense Agent",
    description="AI agent for expense tracking",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

FRONTEND_URL = os.getenv("FRONTEND_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        FRONTEND_URL,
    ] if FRONTEND_URL else [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# AUTH
# ============================================================

security = HTTPBearer()


# ============================================================
# CONVERSATION STORAGE
# ============================================================

conversations = {}


# ============================================================
# REQUEST SCHEMA
# ============================================================

class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


# ============================================================
# CHAT
# ============================================================

@app.post("/chat")
def chat(
    request: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    access_token = credentials.credentials

    # Create a new conversation if one doesn't exist
    conversation_id = (
        request.conversation_id
        or str(uuid4())
    )

    # Get existing conversation or create one
    conversation = conversations.setdefault(
        conversation_id,
        {
            "messages": [],
            "pending_delete": None,
            "pending_edit": None,
            "pending_selection": None,
        }
    )

    # Run the AI agent
    result = run_agent(
        user_input=request.message,
        access_token=access_token,
        conversation=conversation["messages"],
        pending_delete=conversation["pending_delete"],
        pending_edit=conversation["pending_edit"],
        pending_selection=conversation["pending_selection"],
    )

    # Save pending actions
    conversation["pending_delete"] = result.get(
        "pending_delete"
    )

    conversation["pending_edit"] = result.get(
        "pending_edit"
    )

    conversation["pending_selection"] = result.get(
        "pending_selection"
    )

    # Return the actual agent response
    return {
        "response": result["response"],
        "conversation_id": conversation_id,
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AI Expense Agent is running"
    }