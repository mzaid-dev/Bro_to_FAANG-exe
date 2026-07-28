from prompt_contract.application.extract_placeholders import (
    extract_placeholders,
)


def test_extract_single_placeholder():
    assert extract_placeholders(
        "Hello {name}"
    ) == {"name"}


def test_extract_multiple_placeholders():
    assert extract_placeholders(
        "{name} works at {company}"
    ) == {"name", "company"}


def test_extract_no_placeholder():
    assert extract_placeholders(
        "Hello World"
    ) == set()