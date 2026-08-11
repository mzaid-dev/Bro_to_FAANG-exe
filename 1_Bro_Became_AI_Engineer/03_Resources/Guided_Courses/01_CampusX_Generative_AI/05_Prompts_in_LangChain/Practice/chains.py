# chains_demo.py

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableBranch
from dotenv import load_dotenv
import os

load_dotenv()

# Model
model = ChatGroq(
    model=os.getenv("GROQ_MODEL"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

parser = StrOutputParser()


# ==========================================================
# 1. SIMPLE CHAIN
# Prompt → Model → Parser
# Flow
#      A → B
# ==========================================================

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in one sentence."
)

simple_chain = prompt | model | parser

print(simple_chain.invoke({"topic": "RAG"}))


# ==========================================================
# 2. SEQUENTIAL CHAIN
# Step 1 → Step 2 → Step 3
# Flow 
#      A → B → C
# ==========================================================

generate = ChatPromptTemplate.from_template(
    "Give a short explanation of {topic}."
) | model | parser

improve = ChatPromptTemplate.from_template(
    "Improve this explanation:\n{text}"
) | model | parser

sequential_chain = generate | (
    lambda text: {"text": text}
) | improve

print(sequential_chain.invoke({"topic": "LLM"}))


# ==========================================================
# 3. PARALLEL CHAIN
# Same input → multiple independent chains
# Flow 
#             ┌→ B
#      A ─────┼→ C
#             └→ D
# ==========================================================

summary = ChatPromptTemplate.from_template(
    "Summarize {topic} in one sentence."
) | model | parser

keywords = ChatPromptTemplate.from_template(
    "Give 3 keywords for {topic}."
) | model | parser

parallel_chain = RunnableParallel(
    summary=summary,
    keywords=keywords
)

print(parallel_chain.invoke({"topic": "LangChain"}))


# ==========================================================
# 4. CONDITIONAL CHAIN
# Input → condition → choose a chain
# Flow
#             ┌→ B
#      A → Router
#             └→ C
# ==========================================================

coding_chain = ChatPromptTemplate.from_template(
    "Answer this coding question:\n{input}"
) | model | parser

general_chain = ChatPromptTemplate.from_template(
    "Answer this general question:\n{input}"
) | model | parser

router = RunnableBranch(
    (
        lambda x: "python" in x["input"].lower(),
        coding_chain
    ),
    general_chain  # Default/fallback chain
)

print(router.invoke({
    "input": "Write a Python hello world program"
}))