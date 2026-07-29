from google import genai

from llm_gateway.infrastructure.settings import settings


class GeminiAdapter:
    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is missing")

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    async def generate(self, prompt: str) -> str:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        response = await self.client.aio.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response")

        return response.text