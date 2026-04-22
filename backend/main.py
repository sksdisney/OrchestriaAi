from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: int
    message: str

class ChatResponse(BaseModel):
    status: str
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Placeholder for actual chat processing logic
    response_message = f"Echo: {request.message}"
    return ChatResponse(status="success", response=response_message)