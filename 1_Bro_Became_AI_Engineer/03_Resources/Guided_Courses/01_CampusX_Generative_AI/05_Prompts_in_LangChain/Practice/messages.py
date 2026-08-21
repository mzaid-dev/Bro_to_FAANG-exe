from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from model import client

messages = [
    SystemMessage(
        content="You are you helpfull Ai"
    ),
    HumanMessage(
        content="Tell me about the langchain"
    )
]


result = client.invoke(messages)

messages.append(
    AIMessage(
        content=result.content
    )
)


print(messages)