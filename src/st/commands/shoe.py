from rich.console import Console
from ..util.shoe_util import compute_total_miles

console = Console()

def shoe() -> None:
    """Print total miles on Brooks Ghost shoes."""
    total_miles = compute_total_miles()
    console.print(f"Total miles on shoes: {round(total_miles, 2)}")