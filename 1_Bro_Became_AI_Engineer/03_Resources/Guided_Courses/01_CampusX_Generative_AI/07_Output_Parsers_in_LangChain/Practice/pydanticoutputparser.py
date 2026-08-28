from model import client
from langchain_classic.output_parsers import (
    PydanticOutputParser
)
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

class Person(BaseModel):
    name : str = Field(description="Name of the person")
    age : int = Field(description="Age of the person")
    city : str = Field(description="Name of the city belongs to")

parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template="Generate the name, age and city of the fictional {place} person \n {format_instruction}",
    input_variables=["place"],
    partial_variables={'format_instruction' : parser.get_format_instructions()}   
)


# Without using a chain
# prompt = template.invoke({'plce':'Pakistan'})
# result = client.invoke(prompt)
# final_result = parser.parse(result.content)


# Using an LCEL (LangChain Expression Language) chain:
# PromptTemplate -> Model -> JsonOutputParser
chain = template | client | parser

final_result = chain.invoke({'plce':'Pakistan'})

print(type(final_result))
print(final_result)
print(final_result.name)
