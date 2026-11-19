import os 
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()
MODEL = os.getenv("LLM_MODEL")

def ask_llm(message: str, history) -> str:
    messages = history + [{"role": "user", "content": message}]
    completion = client.chat.completions.create(
    model=MODEL,
    messages=messages)
    return completion.choices[0].message.content