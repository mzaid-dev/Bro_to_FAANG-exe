import asyncio
import typer
from typing import Annotated

from llm_gateway.application.generate_text import GenerateText
from llm_gateway.infrastructure.gemini_adapter import GeminiAdapter

cli = typer.Typer()


async def generate_text(prompt: str) -> str:
    provider = GeminiAdapter()
    use_case = GenerateText(provider)

    return await use_case.execute(prompt)


@cli.command()
def main(
    prompt: Annotated[
        str,
        typer.Argument(
            help="Prompt that will be sent to the LLM",
        ),
    ],
):
    response = asyncio.run(generate_text(prompt))
    typer.echo(response)


if __name__ == "__main__":
    cli()