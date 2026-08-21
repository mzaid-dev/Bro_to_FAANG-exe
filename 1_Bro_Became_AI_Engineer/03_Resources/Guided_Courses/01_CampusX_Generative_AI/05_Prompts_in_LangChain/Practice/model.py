from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

client = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
)