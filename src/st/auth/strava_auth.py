from flask import Flask, request
import requests
import json
import os
from datetime import datetime
import webbrowser
import time
from ..config.constants import TOKEN_FILE, AUTH_URL
from ..config.constants_secure import CLIENT_SECRET, CLIENT_ID
from .auth_server import create_auth_server
from rich.console import Console

app = Flask(__name__)
console = Console()

def load_token():
    """Load token data from JSON file"""
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'r') as f:
                token_data = json.load(f)
            return token_data
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    return None

def get_headers(token_data):
    """Get headers with authorization token"""
    return {
        'Authorization': f"Bearer {token_data['access_token']}"
}

def is_token_valid(token_data):
    """Check if the token is valid and not expired"""
    if not token_data:
        return False
    
    required_fields = ['access_token', 'expires_at', 'refresh_token']
    if not all(field in token_data for field in required_fields):
        return False
    
    current_time = int(time.time())
    expires_at = token_data.get('expires_at', 0)

    if current_time >= (expires_at - 300):
        return False
    
    return True

def refresh_token(token_data):
    """Refresh the access token using the refresh token"""
    if not token_data or 'refresh_token' not in token_data:
        return None
    
    refresh_url = 'https://www.strava.com/oauth/token'
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': token_data['refresh_token'],
        'grant_type': 'refresh_token'
    }

    try:
        response = requests.post(refresh_url, data=payload)
        if response.status_code == 200:
            new_token_data = response.json()
            new_token_data['saved_at'] = datetime.now().isoformat()

            with open(TOKEN_FILE, 'w') as f:
                json.dump(new_token_data, f, indent=2)

            print ("Token refreshed successfully!")
            return new_token_data
        else:
            print(f"Failed to refresh token: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error refreshing token: {e}")
        return None
        
def authenticate():
    """Handle the authentication flow"""
    print("No valid token found. Redirecting to Strava authorization")
    print(f"Please visit: {AUTH_URL}")
    print("\nAfter authorization, the token will be saved automatically.")
    
    auth_server = create_auth_server()
    if not auth_server.start_server():
        print("failed to start authentication server")
        return False

    try:
        webbrowser.open(AUTH_URL)
        success = auth_server.wait_for_token(timeout=300)
        print("\nAuthorization page opened in your browser.")

    finally:
        auth_server.stop_server()

    return False

def authenticate_user():
    """Main function to check token and handle authentication"""
    console.print("Checking Strava token...")

    token_data = load_token()

    if is_token_valid(token_data):
        console.print("Valid token found!")
        console.print(f"Token expires at: {datetime.fromtimestamp(token_data['expires_at'])}")
    else:
        if token_data and 'refresh_token' in token_data:
            console.print("Token expired. Attempting to refresh...")
            refreshed_token = refresh_token(token_data)
            if refreshed_token and is_token_valid(refreshed_token):
                console.print("New token refreshed successfully!")
                console.print(f"New token expires at: {datetime.fromtimestamp(refreshed_token['expires_at'])}")
                return
        if not authenticate():
            return False

    return token_data