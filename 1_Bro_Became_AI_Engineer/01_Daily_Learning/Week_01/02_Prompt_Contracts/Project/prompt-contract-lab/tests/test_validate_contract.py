import pytest

from prompt_contract.application.validate_contract import (
    validate_variables,
)


def test_validation_passes():
    validate_variables(
        "Hello {name}",
        {"name": "Zaid"},
    )


def test_validation_fails():
    with pytest.raises(ValueError):
        validate_variables(
            "Hello {name}",
            {},
        )