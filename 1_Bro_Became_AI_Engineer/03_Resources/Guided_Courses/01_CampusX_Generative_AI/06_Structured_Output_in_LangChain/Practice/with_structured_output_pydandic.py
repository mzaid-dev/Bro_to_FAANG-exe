from pydantic import BaseModel, Field
from typing import Literal, Optional
from model import llm
from review_input import review_input
from utility import get_structured_output

# schema
from pydantic import BaseModel, Field
from typing import Optional, Literal


class Review(BaseModel):

    key_themes: list[str] = Field(
        description="List all key themes"
    )

    summary: str = Field(
        description="Brief summary"
    )

    sentiment: Literal["pos", "neg"] = Field(
        description="Review sentiment"
    )

    pros: Optional[list[str]] = Field(
        default=None,
        description="List pros"
    )

    cons: Optional[list[str]] = Field(
        default=None,
        description="List cons"
    )

    reviewer_name: Optional[str] = Field(
        default=None,
        description="Extract only the human author's name. Return None if the review does not contain a person's name."
    )

# from pydantic to json schema
# print(Review.model_json_schema())

result = get_structured_output(llm,Review,review_input)

print(result)
print(result.reviewer_name)
print(type(result))

