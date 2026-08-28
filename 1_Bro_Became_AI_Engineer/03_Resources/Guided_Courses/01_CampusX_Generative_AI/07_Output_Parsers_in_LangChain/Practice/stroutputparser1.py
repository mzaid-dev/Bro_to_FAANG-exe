from langchain_core.prompts import PromptTemplate
from model import client
from langchain_core.output_parsers import StrOutputParser

# 1st Prompt -> Detailed Report
template1 = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=['topic']
)

# 2nd Prompt -> Summary
template2 = PromptTemplate(
    template="Write a 5 line summary on the following text. \n\n {topic}",
    input_variables=['topic']
)

parser = StrOutputParser()

template2 = PromptTemplate(
    template="""Write a 5-line summary of the following text:

{text} """,
    input_variables=["text"]
)

parser = StrOutputParser()

chain = (
    template1
    | client
    | parser
    | template2
    | client
    | parser
)

result = chain.invoke({
    "topic": "LLM evaluation"
})

print(result)
