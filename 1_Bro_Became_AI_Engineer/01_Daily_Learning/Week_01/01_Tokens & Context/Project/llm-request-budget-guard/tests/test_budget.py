from llm_budget.domain.budget import (
    RequestBudget,
    allowed_input,
)


def test_allowed_input():
    budget = RequestBudget(
        max_input_tokens=6000,
        reserved_output_tokens=1000,
        safety_margin_tokens=256,
    )

    result = allowed_input(
        provider_input_limit=8000,
        context_capacity=8192,
        budget=budget,
    )

    assert result == 6000