from app.models.logs import AILogs
from app.core.db import get_session
from sqlmodel import Session, select, desc, func

# Business logic for logging operations.

def save_log_to_db(user_id: int, prompt: str, response: str, tokens: int):
    new_log = AILogs(
        user_id=user_id,
        prompt=prompt,
        response=response,
        tokens_used=tokens,
        agent_name="gpt-3.5-turbo",  # This can be dynamic based on the actual model used,
        success=True  # Assuming success for now, can be updated based on actual response status
    )
    with get_session() as session:
        session.add(new_log)
        session.commit()

class LogService:
    @staticmethod
    def get_paginated_logs(session: Session, page: int, size: int, agent: str = None):
        skip = (page - 1) * size
        
        # Build query
        statement = select(AILogs).order_by(desc(AILogs.created_at))
        if agent:
            statement = statement.where(AILogs.agent_name == agent)
        
        # Get count and data
        total_count = session.exec(select(func.count()).select_from(AILogs)).one()
        results = session.exec(statement.offset(skip).limit(size)).all()
        
        return {
            "logs": results,
            "total": total_count,
            "page": page,
            "size": size,
            "total_pages": (total_count + size - 1) // size
        }
