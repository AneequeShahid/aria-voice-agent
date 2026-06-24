"""FastAPI chat endpoint for Telegram / future integration."""

import os

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from aria.brain import run_brain

load_dotenv()
app = FastAPI(title="Aria Voice Agent API")


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    response: str
    session_id: str


@app.get("/health")
def health():
    return {"status": "ok", "agent": "aria"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    answer = run_brain(req.message, session_id=req.session_id)
    return ChatResponse(response=answer, session_id=req.session_id)


@app.post("/reset/{session_id}")
def reset(session_id: str):
    return {"status": "ok", "session_id": session_id, "message": "new session started"}
