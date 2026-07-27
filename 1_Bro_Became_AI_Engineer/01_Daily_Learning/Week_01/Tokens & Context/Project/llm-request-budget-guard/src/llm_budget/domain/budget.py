from dataclasses import dataclass

@dataclass(frozen=True)
class RequestBudget:
    max_input_tokens: int
    reserved_output_tokens: int
    safety_margin_tokens: int

@dataclass(frozen=True)
class ModelPricing:
    input_cost_per_million: float
    output_cost_per_million: float

def allowed_input(
    *,
    provider_input_limit: int,
    context_capacity: int,
    budget: RequestBudget,
) -> int:
    """
    Calculate the maximum safe number of input tokens.
    """

    context_limit = max(
        0,
        context_capacity
        - budget.reserved_output_tokens
        - budget.safety_margin_tokens,
    )

    return min(
        provider_input_limit,
        budget.max_input_tokens,
        context_limit,
    )

@dataclass(frozen=True)
class BudgetReport:
    characters: int
    words: int
    input_tokens: int
    allowed_input_tokens: int
    remaining_input_tokens: int
    reserved_output_tokens: int

    estimated_input_cost: float
    estimated_output_cost: float
    estimated_total_cost: float

    accepted: bool
    reasons: list[str]

