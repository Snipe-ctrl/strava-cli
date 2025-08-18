from functools import wraps
from rich.console import Console
from .strava_auth import load_token, is_token_valid, refresh_token, authenticate

console = Console()

def require_auth(func):
    """Decorator to require authentication before running a command"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if user is authenticated
        token_data = load_token()
        
        if not token_data:
            console.print("[red]❌ You are not logged in to Strava![/red]")
            console.print("Run [bold]st login[/bold] to authenticate with Strava.")
            return None
        
        if not is_token_valid(token_data):
            # Try to refresh the token
            if 'refresh_token' in token_data:
                console.print("[yellow]🔄 Token expired. Attempting to refresh...[/yellow]")
                refreshed_token = refresh_token(token_data)
                if refreshed_token and is_token_valid(refreshed_token):
                    console.print("[green]✅ Token refreshed successfully![/green]")
                else:
                    console.print("[red]❌ Failed to refresh token. Please log in again.[/red]")
                    console.print("Run [bold]st login[/bold] to re-authenticate with Strava.")
                    return None
            else:
                console.print("[red]❌ Invalid token. Please log in again.[/red]")
                console.print("Run [bold]st login[/bold] to authenticate with Strava.")
                return None
        
        # User is authenticated, proceed with the command
        return func(*args, **kwargs)
    
    return wrapper
