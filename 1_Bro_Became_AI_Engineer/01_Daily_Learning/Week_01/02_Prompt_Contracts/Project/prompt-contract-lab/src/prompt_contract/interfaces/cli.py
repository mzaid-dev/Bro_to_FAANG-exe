import typer

from prompt_contract.application.render_contract import (
    render_contract,
)
from prompt_contract.infrastructure.contracts import (
    DEFAULT_CONTRACT,
)

app = typer.Typer()


@app.command()
def render(
    question: str,
    context: str = "",
):
    """
    Render a Prompt Contract.
    """

    prompt = render_contract(
        DEFAULT_CONTRACT,
        {
            "question": question,
            "context": context,
        },
    )

    typer.echo(prompt)


if __name__ == "__main__":
    app()