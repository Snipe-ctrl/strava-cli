from rich.console import Console
from ..auth.decorators import require_auth
from ..util.miles_util import compute_total_miles

console = Console()

@require_auth
def miles() -> None:
    """Print total amount of recorded miles ran."""
    total_miles = compute_total_miles()
    console.print(f"Total miles ran over all time: {round(total_miles, 2)}")