from model import client
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

chat_history = [
    SystemMessage(
        content="You are a helpful AI assistant"
    ),
]

while True:
    print("You: ", end="", flush=True)
    user_prompt = input()

    print("AI: ", end="", flush=True)

    output = ""

    for chunk in client.stream(chat_history):
        if chunk.content:
            output += chunk.content
            print(chunk.content, end="", flush=True)

    chat_history.extend([
        HumanMessage(
            content=user_prompt
        ),
        AIMessage(
            content=output
        )
    ])

    print()