from prompt_contract.application.render_contract import (
    render_contract,
)

from prompt_contract.infrastructure.contracts import (
    DEFAULT_CONTRACT,
)


def test_render_contract():

    prompt = render_contract(
        DEFAULT_CONTRACT,
        {
            "question": "What is AI?",
            "context": "Artificial Intelligence",
        },
    )

    assert "What is AI?" in prompt
    assert "Artificial Intelligence" in prompt
    assert "Senior AI Assistant" in prompt