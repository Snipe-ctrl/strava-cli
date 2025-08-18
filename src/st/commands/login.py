from rich.console import Console
from ..auth.strava_auth import authenticate_user

console = Console()

def login() -> None:
    if not authenticate_user():
        console.print("Failed to log user in")
    console.print("User logged in successfully!")
