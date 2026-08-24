from typing import TypedDict, Annotated, Optional
from model import llm
from review_input import review_input
from utility import get_structured_output

# schema
class Review(TypedDict):

    key_themes : Annotated[list[str] ,"write down all the key themes discused in the review in the list."]
    summary : Annotated[str, "A brief summary of the review."]
    sentiment : Annotated[str, "Return sentiment of the review either negative or positive or neutral"]
    pros: Annotated[Optional[list[str]], "Write down all the pross inside a list"]
    cons: Annotated[Optional[list[str]], "Write down all the cons inside a list"]


result = get_structured_output(llm,Review,review_input)

print(result)
print(type(result))
print(result['summary'])
print(result['sentiment'])
