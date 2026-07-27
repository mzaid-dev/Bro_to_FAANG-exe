from dataclasses import dataclass
from llm_budget.domain.budget import (
    RequestBudget,
    BudgetReport,
    ModelPricing,
    allowed_input,
)
from llm_budget.ports.token_counter import TokenCounter

def assess_request(
    text: str,
    counter: TokenCounter,
    budget: RequestBudget,
    pricing: ModelPricing,
    provider_input_limit: int,
    context_capacity: int,
) -> BudgetReport:
    
    characters = len(text)
    words = len(text.split())
    input_tokens = counter.count(text) 

    allowed = allowed_input(
        provider_input_limit=provider_input_limit,
        context_capacity=context_capacity,
        budget=budget,
    )

    accepted = input_tokens <= allowed

    reasons = []

    if not accepted:
        reasons.append("Input exceeds allowed token budget.")

    remaining = allowed - input_tokens

    estimated_input_cost = (
    input_tokens / 1_000_000
    ) * pricing.input_cost_per_million

    estimated_output_cost = (
        budget.reserved_output_tokens / 1_000_000
    ) * pricing.output_cost_per_million

    estimated_total_cost = (
        estimated_input_cost
        + estimated_output_cost
    )

    return BudgetReport(
        characters=characters,
        words=words,
        input_tokens=input_tokens,
        allowed_input_tokens=allowed,
        remaining_input_tokens=remaining,
        reserved_output_tokens=budget.reserved_output_tokens,
        estimated_input_cost=estimated_input_cost,
        estimated_output_cost=estimated_output_cost,
        estimated_total_cost=estimated_total_cost,
        accepted=accepted,
        reasons=reasons,
    )