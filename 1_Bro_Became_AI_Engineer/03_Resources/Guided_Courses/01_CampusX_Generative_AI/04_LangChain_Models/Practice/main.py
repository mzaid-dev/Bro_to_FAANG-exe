# from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# load_dotenv()

# llm = ChatOpenAI(
#     model=os.getenv("OPENAI_MODEL"),
#     api_key=os.getenv("OPENAI_API_KEY"),
# )


# responce = llm.invoke("Write a hello world in python >")

# print(responce.content)


from langchain_nvidia_ai_endpoints import ChatNVIDIA

client = ChatNVIDIA(
    model=os.getenv("OPENAI_MODEL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

response = client.invoke("Write hello world in assembly language >")

print("Response : "+response.content)