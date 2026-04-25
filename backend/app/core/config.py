import os
import logging
from dotenv import load_dotenv

def load_env():
    # Setup Logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    # Load the .env file
    load_dotenv()
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY. Did you forget to create a .env file?")
    return api_key

# Configuration, environment variable loading, etc.
