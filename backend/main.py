import logging
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

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

app = FastAPI()

# Allow your frontend to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=api_key)

class ChatRequest(BaseModel):
    user_id: int
    message: str

class ChatResponse(BaseModel):
    status: str
    response: str

# Simple in-memory storage: { user_id: [messages] }
chat_storage: Dict[int, List[Dict[str, str]]] = {}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
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

        return ChatResponse(status="success", response=ai_reply)
    # Placeholder for actual chat processing logic
    except Exception as e:
        # 3. Error Handling - Catching API issues, timeouts, etc.
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="The AI is currently taking a nap. Try again later.")