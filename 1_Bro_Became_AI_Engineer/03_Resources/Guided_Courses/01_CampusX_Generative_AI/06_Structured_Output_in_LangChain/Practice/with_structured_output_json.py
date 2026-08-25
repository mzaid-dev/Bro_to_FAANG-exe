from model import llm
from review_input import review_input
from utility import get_structured_output
from with_structured_output_pydandic import Review

json_schema = Review.model_json_schema()

result = llm.with_structured_output(
    json_schema,
    review_input
)

print(result)