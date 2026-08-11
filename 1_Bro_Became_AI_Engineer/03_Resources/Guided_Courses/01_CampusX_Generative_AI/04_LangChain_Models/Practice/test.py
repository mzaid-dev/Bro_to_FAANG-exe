# import langchain

# print(langchain.__version__)

from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
import os

load_dotenv()

client = ChatDeepSeek(
    model=os.getenv("DEEPSEEK_MODEL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

while True:
    user_prompt = input("You: ")

    if user_prompt.strip().lower() == "exit":
        print("Goodbye!")
        break

    if not user_prompt.strip():
        continue

    response = client.stream(user_prompt.strip())

    print("Bot: ", end="", flush=True)
    for chunk in response:
    
        print(chunk.content, end="", flush=True)
    
    print("\n")