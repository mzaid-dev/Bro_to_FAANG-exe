import json
import typer
from dataclasses import asdict

from llm_budget.application.assess_request import assess_request
from llm_budget.domain.budget import (
    RequestBudget,
    ModelPricing,
)
from llm_budget.infrastructure.provider_counter import MockTokenCounter


app = typer.Typer()


@app.command()
def check(text : str):
    budget = RequestBudget(
        max_input_tokens=6000,
        reserved_output_tokens=1000,
        safety_margin_tokens=256,
    )

    pricing = ModelPricing(
        input_cost_per_million=0.40,
        output_cost_per_million=1.60,
    )

    report = assess_request(
    text=text,
    counter=MockTokenCounter(),
    budget=budget,
    pricing=pricing,
    provider_input_limit=8000,
    context_capacity=8192,
    )

    typer.echo(json.dumps(asdict(report), indent=2))


if __name__ == "__main__":
    app()