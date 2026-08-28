from model import client
from langchain_core.output_parsers import JsonOutputParser
from utility import parsing
from langchain_core.prompts import PromptTemplate

# JsonOutputParser parses JSON output, but it does not enforce a custom schema by itself.
# If we need a predefined schema, we can use a schema-based parser such as PydanticOutputParser, StructuredOutputParser.
parser = JsonOutputParser()

template = PromptTemplate(
    template="Give me the name, age, city of the fictional person \n {format_instruction}",
    input_variables=[],
    # partial_variables are values that are filled into the prompt in advance,
    # so we do not need to provide them again when invoking the prompt.
    partial_variables={'format_instruction' : parser.get_format_instructions()}
)


# Without using a chain
# prompt = template.format()
# result = client.invoke(prompt)
# final_result = parser.parse(result.content)

# Using an LCEL (LangChain Expression Language) chain:
# PromptTemplate -> Model -> JsonOutputParser
chain = template | client | parser

# invoke() expects an input value.
# Since this prompt has no runtime input variables, we pass an empty dictionary.
final_result = chain.invoke({})

print(final_result)
print(type(final_result))

print(final_result['name'])