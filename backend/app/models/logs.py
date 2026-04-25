from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class AILogs(SQLModel, table=True):
    __tablename__ = "ai_logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    prompt: str
    response: str
    tokens_used: int
    agent_name: str = Field(index=True)
    success: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
