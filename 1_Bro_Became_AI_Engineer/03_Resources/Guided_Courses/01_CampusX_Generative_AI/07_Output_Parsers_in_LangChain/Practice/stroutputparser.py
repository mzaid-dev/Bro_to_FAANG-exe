from langchain_core.prompts import PromptTemplate
from model import client

# 1st Prompt -> Detailed Report
template1 = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=['topic']
)

# 2nd Prompt -> Summary
template2 = PromptTemplate(
    template="Write a 5 line summary on the following text. /n {topic}",
    input_variables=['topic']
)

prompt1 = template1.invoke({'topic': 'LLM evaluation'})

result = client.invoke(prompt1)

prompt2 = template2.invoke({'topic': result.content})

f_result = client.invoke(prompt2)

print(f_result.content)