# Business logic for OpenAI interactions.

import os
from openai import OpenAI
from app.core.config import load_env

api_key = os.getenv("OPENAI_API_KEY") or load_env()
client = OpenAI(api_key=api_key)

def get_openai_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ai_reply = response.choices[0].message.content
    tokens = response.usage.total_tokens
    return ai_reply, tokens
