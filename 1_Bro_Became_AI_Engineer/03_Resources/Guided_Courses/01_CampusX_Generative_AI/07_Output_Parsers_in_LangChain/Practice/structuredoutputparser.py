from model import client
from langchain_core.output_parsers import JsonOutputParser
from utility import parsing
# langchain_core contains LangChain's essential building blocks and core abstractions
from langchain_core.prompts import PromptTemplate
from langchain_classic.output_parsers.structured import (
    StructuredOutputParser,
    ResponseSchema
)

schema = [
    ResponseSchema(name="fact_1",description='Fact 1 about the topic'),
        ResponseSchema(name="fact_2",description='Fact 2 about the topic'),
            ResponseSchema(name="fact_3",description='Fact 3 about the topic')
]

parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(
    template="Give me 3 fact about {topic} \n {format_instruction}",
    input_variables=["topic"],
    partial_variables={'format_instruction' : parser.get_format_instructions()}
)


# Without using a chain
# prompt = template.invoke({'topic': "llm evaluation"})
# result = client.invoke(prompt)
# final_result = parser.invoke(result.content)

# Using an LCEL (LangChain Expression Language) chain:
# PromptTemplate -> Model -> JsonOutputParser
chain = template | client | parser

final_result = chain.invoke({"topic" : "llm evaluation"})

print(final_result)
print(type(final_result))

print(final_result['fact_1'])

