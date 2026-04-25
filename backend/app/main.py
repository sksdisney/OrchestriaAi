from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import chat
from app.api.v1 import logs
from app.core.config import load_env

# Load environment variables
load_env()

app = FastAPI()

# Allow your frontend to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(logs.router, prefix="/api/v1/logs", tags=["Logs"])

# Startup event for DB
from app.core.db import create_db_and_tables

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
