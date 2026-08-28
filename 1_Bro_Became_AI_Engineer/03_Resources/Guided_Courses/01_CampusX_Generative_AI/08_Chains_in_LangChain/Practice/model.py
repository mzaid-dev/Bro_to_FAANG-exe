from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

client = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model="openai/gpt-oss-120b"
)

