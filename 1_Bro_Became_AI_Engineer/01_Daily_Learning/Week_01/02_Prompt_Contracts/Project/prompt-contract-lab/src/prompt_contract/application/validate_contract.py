from prompt_contract.application.extract_placeholders import (
    extract_placeholders,
)


def validate_variables(
    template: str,
    variables: dict[str, str],
) -> None:
    """
    Ensure every placeholder in the template
    has a matching variable.
    """

    required = extract_placeholders(template)

    missing = required - variables.keys()

    if missing:
        raise ValueError(
            f"Missing variables: {', '.join(sorted(missing))}"
        )