from typing import TypedDict
from model import llm
from review_input import review_input
from utility import get_structured_output

# schema
class Review(TypedDict):

    summary : str
    sentiment : str


result = get_structured_output(llm,Review,review_input)

print(result)
# print(result['summary'])
# print(result['sentiment'])


