import os
from dotenv import load_dotenv


load_dotenv()


class Settings:

    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")


        self.llm_provider = os.getenv(
            "LLM_PROVIDER",
            "gemini"
        )

        self.timeout = int(
            os.getenv(
                "LLM_TIMEOUT_SECONDS",
                20
            )
        )


settings = Settings()