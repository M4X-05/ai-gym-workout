import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

# Get OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Debugging: Check if API key is loaded correctly
if openai.api_key:
    print(f"✅ API Key Loaded: {openai.api_key[:5]}... (hidden for security)")
else:
    print("🚨 Error: API Key not found. Check your .env file.")

# Test OpenAI API connection (Updated for OpenAI v1+)
try:
    response = openai.Client().models.list()
    print("✅ OpenAI API Key is valid and working!")
except openai.OpenAIError as e:
    print(f"🚨 API Error: {e}")
