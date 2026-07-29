import pytest

from llm_gateway.infrastructure.gemini_adapter import GeminiAdapter


@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
async def test_gemini_generate():

    llm = GeminiAdapter()


    response = await llm.generate(
        "Explain python in one line"
    )

    print("Gemini response:", response)

    assert response is not None
    assert isinstance(response, str)
    assert response.strip() != ""
