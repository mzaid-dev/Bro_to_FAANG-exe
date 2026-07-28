from llm_budget.application.assess_request import assess_request
from llm_budget.domain.budget import RequestBudget
from llm_budget.infrastructure.provider_counter import MockTokenCounter
from llm_budget.domain.budget import ModelPricing



budget = RequestBudget(
    max_input_tokens=10,
    reserved_output_tokens=0,
    safety_margin_tokens=0,
)

pricing = ModelPricing(
    input_cost_per_million=0.40,
    output_cost_per_million=1.60,
)

def test_accept_below_limit():
    report = assess_request(
        text="a" * 36,   # 36 // 4 = 9 tokens
        counter=MockTokenCounter(),
        budget=budget,
        provider_input_limit=10,
        context_capacity=10,
        pricing=pricing,
    )

    assert report.accepted is True


def test_accept_at_limit():
    report = assess_request(
        text="a" * 40,   # 40 // 4 = 10 tokens
        counter=MockTokenCounter(),
        budget=budget,
        provider_input_limit=10,
        context_capacity=10,
        pricing=pricing,
    )

    assert report.accepted is True


def test_reject_above_limit():
    report = assess_request(
        text="a" * 44,   # 44 // 4 = 11 tokens
        counter=MockTokenCounter(),
        budget=budget,
        provider_input_limit=10,
        context_capacity=11,
        pricing=pricing,
    )

    assert report.accepted is False