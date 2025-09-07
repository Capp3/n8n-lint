"""Console script for n8n_lint."""

import typer
from rich.console import Console

from n8n_lint import utils

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for n8n_lint."""
    console.print("Replace this message by putting your code into "
               "n8n_lint.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()


if __name__ == "__main__":
    app()
