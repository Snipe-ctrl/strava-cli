from __future__ import annotations

import typer
from typing import Optional
from . import __version__
from rich.console import Console

console = Console()
app = typer.Typer(
    add_completion=False,
    help="st Typer CLI boilerplate"
)

def version_callback(value: bool):
    if value:
        console.print(f"st [bold]{__version__}[/bold]")
        raise typer.Exit()
    
@app.callback(no_args_is_help=True)
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
):
    """Top level CLI. Use subcommands like 'st hello'.

    Tip: run 'mc --help and 'python -m st --help."""

@app.command()
def hello(name: str = typer.Argument("world")) -> None:
    """Say hello."""
    console.print(f"Hello, [bold]{name}[/bold]!")

from .commands.shoe import shoe as shoe_cmd
app.command("shoe")(shoe_cmd)

from .commands.login import login as login_cmd
app.command("login")(login_cmd)

