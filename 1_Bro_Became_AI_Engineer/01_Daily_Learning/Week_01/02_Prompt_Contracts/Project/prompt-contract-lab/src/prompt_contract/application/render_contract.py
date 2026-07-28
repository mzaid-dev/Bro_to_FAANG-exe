from prompt_contract.domain.contract import PromptContract

from prompt_contract.application.validate_contract import (
    validate_variables,
)


def render_contract(
    contract: PromptContract,
    variables: dict[str, str],
) -> str:
    """
    Render a Prompt Contract into the final prompt.
    """

    validate_variables(contract.input_template, variables)

    rendered_input = contract.input_template.format(**variables)

    rules = "\n".join(
        f"- {rule}" for rule in contract.instructions
    )

    return f"""
========================
Prompt Contract
========================

Version:
{contract.version}

ROLE
{contract.role}

OBJECTIVE
{contract.objective}

RULES
{rules}

INPUT
{rendered_input}

OUTPUT FORMAT
{contract.output_template}
""".strip()