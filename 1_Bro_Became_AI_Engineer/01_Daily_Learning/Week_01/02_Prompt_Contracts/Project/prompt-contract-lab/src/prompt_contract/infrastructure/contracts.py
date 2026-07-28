from prompt_contract.domain.contract import PromptContract


DEFAULT_CONTRACT = PromptContract(
    role="Senior AI Assistant",

    objective=(
        "Answer the user's question accurately using the provided context."
    ),

    instructions=[
        "Never hallucinate.",
        "Use only the supplied context.",
        "If information is missing, say you do not know.",
        "Be concise and clear.",
    ],

    input_template="""
Question:
{question}

Context:
{context}
""".strip(),

    output_template="""
Answer in Markdown.

Sections:
- Answer
- Explanation
- References (if available)
""".strip(),

    version="v1.0",
)