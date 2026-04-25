import logging
import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from sqlmodel import Field, SQLModel, create_engine, Session
from datetime import datetime
from typing import Optional

# 1. Setup Logging - Helps you see what's happening in the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. Load the .env file
load_dotenv() 

# 3. Access the variable using os.getenv
# This looks into your system environment where load_dotenv just placed your key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Missing OPENAI_API_KEY. Did you forget to create a .env file?")

# This class defines the table structure in PostgreSQL
class AILogs(SQLModel, table=True):
    __tablename__ = "ai_logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    prompt: str
    response: str
    tokens_used: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

app = FastAPI()

# Allow your frontend to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection setup
# 'db' is the service name from your docker-compose.yml
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DATABASE_URL)

# This creates the table if it doesn't exist
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Ensure this "startup" event is present
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

client = OpenAI(api_key=api_key)

class ChatRequest(BaseModel):
    user_id: int
    message: str

class ChatResponse(BaseModel):
    status: str
    response: str

# Simple in-memory storage: { user_id: [messages] }
chat_storage: Dict[int, List[Dict[str, str]]] = {}

def save_log_to_db(user_id: int, prompt: str, response: str, tokens: int):
    # Create an instance of our model
    new_log = AILogs(
        user_id=user_id,
        prompt=prompt,
        response=response,
        tokens_used=tokens
    )
    
    # Save it using a Session
    with Session(engine) as session:
        session.add(new_log)
        session.commit()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    logger.info(f"Received chat message: {request.message}")
    user_id = request.user_id
    user_message = request.message

    if user_id not in chat_storage:
        chat_storage[user_id] = [
            {"role": "system", "content": "You are a helpful assistant named OrchestriaAI."}
        ]
        
    # 2. Add the new user message to history
    chat_storage[user_id].append({"role": "user", "content": user_message})  
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_storage[user_id]
        )
        
        ai_reply = response.choices[0].message.content
        logger.info("OpenAI request successful")

        # 4. Add AI's response to history so it remembers next time
        chat_storage[user_id].append({"role": "assistant", "content": ai_reply})

        tokens = response.usage.total_tokens

        # Trigger background task using the SQLModel function
        background_tasks.add_task(save_log_to_db, request.user_id, request.message, ai_reply, tokens)

        return ChatResponse(status="success", response=ai_reply)
    # Placeholder for actual chat processing logic
    except Exception as e:
        # 3. Error Handling - Catching API issues, timeouts, etc.
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="The AI is currently taking a nap. Try again later.")