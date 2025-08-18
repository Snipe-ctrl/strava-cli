import typer
from rich.console import Console
from ..util.shoe_util import compute_total_miles
from ..auth.decorators import require_auth

console = Console()

@require_auth
def shoe() -> None:
    """Print total miles on Brooks Ghost shoes."""
    total_miles = compute_total_miles()
    console.print(f"Total miles on shoes: {round(total_miles, 2)}")