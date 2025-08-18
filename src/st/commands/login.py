from rich.console import Console
from ..auth.strava_auth import authenticate_user

console = Console()

def login() -> None:
    """Log user into Strava."""
    authenticate_user()
    console.print("User logged in successfully!")
