from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import streamlit as st
from langchain_core.prompts import load_prompt

load_dotenv()

client = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    max_retries=2
)

st.header("Research Tool")

with st.form("research_form"):

    paper_input = st.selectbox(
        "Select Research Paper Name",
        [
            "Attention Is All You Need",
            "BERT: Pre-training of Deep Bidirectional Transformers",
            "GPT-3: Language Models are Few-Shot Learners",
            "Diffusion Models Beat GANs on Image Synthesis",
        ],
    )

    style_input = st.selectbox(
        "Select Explanation Style",
        [
            "Beginner-Friendly",
            "Technical",
            "Code-Oriented",
            "Mathematical",
        ],
    )

    length_input = st.selectbox(
        "Select Explanation Length",
        [
            "Short (1-2 paragraphs)",
            "Medium (3-5 paragraphs)",
            "Long (detailed explanation)",
        ],
    )

    submitted = st.form_submit_button("Summarize")


if submitted:

    template = load_prompt("template.json")

    chain = template | client

    response = chain.stream(
        {
            "paper_input": paper_input,
            "style_input": style_input,
            "length_input": length_input,
        }
    )

    output = ""
    placeholder = st.empty()

    for chunk in response:
        output += chunk.content
        placeholder.markdown(output)
    print("===== STREAM FINISHED =====")