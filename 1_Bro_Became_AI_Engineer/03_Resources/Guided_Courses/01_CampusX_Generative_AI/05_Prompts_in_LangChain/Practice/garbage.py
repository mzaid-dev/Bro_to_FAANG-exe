from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-4B-Instruct-2507",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HF_TOKEN"),
    max_new_tokens=1024,
    temperature=0.7,
)


client = ChatGroq( 
    model= "openai/gpt-oss-120b", 
    api_key=os.getenv("GROQ_API_KEY"), 
)



# chat = ChatHuggingFace(llm=llm)

while True:
    print("Bot: ", end="", flush=True)

    user_input = input()

    if user_input == "exit":
        break

    for chunk in client.stream(user_input):
        if chunk.content:
            print(chunk.content, end="", flush=True)

    print()