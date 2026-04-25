from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.schemas.log_schema import ChatRequest, ChatResponse
from app.services.openai_service import get_openai_response
from app.services.log_service import save_log_to_db
import logging

router = APIRouter()

# Simple in-memory storage: { user_id: [messages] }
chat_storage = {}

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    logger = logging.getLogger(__name__)
    logger.info(f"Received chat message: {request.message}")
    user_id = request.user_id
    user_message = request.message

    if user_id not in chat_storage:
        chat_storage[user_id] = [
            {"role": "system", "content": "You are a helpful assistant named OrchestriaAI."}
        ]
    chat_storage[user_id].append({"role": "user", "content": user_message})

    try:
        ai_reply, tokens = get_openai_response(chat_storage[user_id])
        logger.info("OpenAI request successful")
        chat_storage[user_id].append({"role": "assistant", "content": ai_reply})
        background_tasks.add_task(save_log_to_db, user_id, user_message, ai_reply, tokens)
        return ChatResponse(status="success", response=ai_reply)
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="The AI is currently taking a nap. Try again later.")
