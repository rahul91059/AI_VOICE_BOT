import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    MODEL_NAME = os.getenv('MODEL_NAME', 'llama3-70b-8192')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    
    # Validate API key
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")
    
    # Voice settings
    VOICE_RATE = 200
    VOICE_VOLUME = 0.9