# Logging endpoints will be defined here.
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.core.db import get_session
from app.services.log_service import LogService
from app.schemas.log_schema import LogPaginationResponse

router = APIRouter()

@router.get("/", response_model=LogPaginationResponse)
def get_logs(
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100),
    agent: str = None,
    session: Session = Depends(get_session)
):
    return LogService.get_paginated_logs(session, page, size, agent)