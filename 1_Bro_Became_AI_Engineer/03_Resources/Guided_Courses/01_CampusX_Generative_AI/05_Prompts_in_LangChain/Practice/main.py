from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import streamlit as st
from langchain_core.prompts import PromptTemplate

load_dotenv()

template = """
Please summarize the research paper titled "{paper_input}" with the following specifications:

Explanation Style: {style_input}
Explanation Length: {length_input}

1. Mathematical:
   - Include relevant mathematical equations if present in the paper.
   - Explain the mathematical concepts using simple, intuitive code snippets where applicable.

2. Analogies:
   - Use relatable analogies to simplify complex ideas.

If certain information is not available in the paper, respond with:
"Insufficient information available" instead of guessing.

Ensure the summary is clear, accurate, and aligned with the provided style and length.
"""

prompt = PromptTemplate(
    input_variables=["paper_input", "style_input", "length_input"],
    template=template
)


client = ChatGroq( 
    model=os.getenv("GROQ_MODEL"), 
    api_key=os.getenv("GROQ_API_KEY"), 
)


st.header("Reasearch Tool")

with st.form("research_form"):

    paper_input = st.selectbox(
        "Select Research Paper Name",
        [
            "Attention Is All You Need",
            "BERT: Pre-training of Deep Bidirectional Transformers",
            "GPT-3: Language Models are Few-Shot Learners",
            "Diffusion Models Beat GANs on Image Synthesis"
        ]
    )

    style_input = st.selectbox(
        "Select Explanation Style",
        [
            "Beginner-Friendly",
            "Technical",
            "Code-Oriented",
            "Mathematical"
        ]
    )

    length_input = st.selectbox(
        "Select Explanation Length",
        [
            "Short (1-2 paragraphs)",
            "Medium (3-5 paragraphs)",
            "Long (detailed explanation)"
        ]
    )

    submitted = st.form_submit_button("Summarize")

    if submitted:
        chain = prompt | client

        response = chain.stream({
            "paper_input": paper_input,
            "style_input": style_input,
            "length_input": length_input
        })

        output = ""
        placeholder = st.empty()

        for chunk in response:
            output += chunk.content
            placeholder.markdown(output)
    





