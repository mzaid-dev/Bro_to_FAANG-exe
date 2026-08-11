from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

client = ChatGroq(
    model=os.getenv("GROQ_MODEL"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

Role = """ROLE:
You are a temperature classifier for an LLM.

TASK:
Analyze the user's prompt and return the best temperature value.

RULES:
- Simple factual question → 0.0
- Normal conversational request → 0.3
- Creative or brainstorming request → 0.7
- Highly creative request → 0.9

OUTPUT:
Return ONLY the numeric temperature.
No explanation.
No words.
No JSON.
"""
    
def choose_temperature(user_prompt: str) -> float:

    response = client.invoke(
        f"{Role}\nUSER PROMPT: {user_prompt}"
    )

    return float(response.content.strip())


def ask_model(user_prompt: str):

    temperature = choose_temperature(user_prompt)

    model = ChatGroq(
        model=os.getenv("GROQ_MODEL"),
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=temperature,
    )

    response = model.stream(user_prompt)

    for chunk in response:
        yield chunk.content

def main():

    while True:

        user_prompt = input("You: ")

        if user_prompt.strip().lower() == "exit":
            print("Goodbye!")
            break

        if not user_prompt.strip():
            continue

        response = ask_model(user_prompt.strip())

        print("Bot: ", end="", flush=True)

        for chunk in response:
            print(chunk, end="", flush=True)

        print("\n")


main()