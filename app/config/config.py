import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Vector store configuration
VECTOR_STORE_PATH = "vector_stores"

# Crew AI configuration
TEMPERATURE = 0.7
MODEL = "gpt-4"  # or "gpt-3.5-turbo" for faster, cheaper responses

# Application configuration
DEBUG = True
LOG_LEVEL = "INFO"
