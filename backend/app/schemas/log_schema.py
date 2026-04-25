from pydantic import BaseModel
from typing import List
from app.models.logs import AILogs

class ChatRequest(BaseModel):
    user_id: int
    message: str

class ChatResponse(BaseModel):
    status: str
    response: str

class LogPaginationResponse(BaseModel):
    logs: List[AILogs]
    total: int
    page: int
    size: int
    total_pages: int
