from llm_gateway.infrastructure.settings import settings


def test_settings():
    assert settings.llm_provider is not None
    assert settings.timeout > 0
    assert settings.gemini_api_key is not None