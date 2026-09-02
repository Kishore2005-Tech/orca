from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from backend.agents.coordinator import CoordinatorAgent

app = FastAPI(title="ORCA API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContextMessage(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    request_id: Optional[str] = None
    user_query: str
    conversation_context: Optional[List[ContextMessage]] = None

coordinator = CoordinatorAgent()

@app.post("/api/v1/query")
async def handle_query(query: QueryRequest):
    response = await coordinator.process_query(query.user_query)
    if query.request_id:
        response["request_id"] = query.request_id
    return response

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}
