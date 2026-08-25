from typing import TypedDict, Annotated, Optional, Literal
from model import llm
from review_input import review_input
from utility import get_structured_output

# schema
class Review(TypedDict):

    key_themes: Annotated[list[str], "List all key themes"]
    summary: Annotated[str, "Brief summary"]
    sentiment: Annotated[Literal["pos","neg"], "Review sentiment"]
    pros: Annotated[Optional[list[str]], "List pros"]
    cons: Annotated[Optional[list[str]], "List cons"]

    reviewer_name: Annotated[
        Optional[str],
        "Extract only the human author's name. Return None if the review does not contain a person's name."
    ]


result = get_structured_output(llm,Review,review_input)

print(result)
print(result['reviewer_name'])
# print(type(result))
# print(result['summary'])
# print(result['sentiment'])
