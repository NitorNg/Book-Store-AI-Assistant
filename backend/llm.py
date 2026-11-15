import os 
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai_Client()
MODEL = os.getenv("LLM_MODEL")

def ask_llm(message: str) -> str:
    response = client.models.generate_content(model = MODEL, contents=message)