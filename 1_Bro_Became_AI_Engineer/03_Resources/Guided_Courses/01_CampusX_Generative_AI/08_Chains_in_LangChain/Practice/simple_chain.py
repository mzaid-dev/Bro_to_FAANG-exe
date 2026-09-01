from model import client
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

template = PromptTemplate(
    template="Generate 5 interesting fact about {topic}",
    input_variables=['topic']
)

# without chain 
# prompt = template.invoke({"topic":"cricket"})
# result = client.invoke(prompt)
# final_result = parser.invoke(result)

# with chain 

chain = template | client | parser

print(chain.invoke({'topic':'LLM evaluation'}))

# print(chain.get_graph().draw_ascii)