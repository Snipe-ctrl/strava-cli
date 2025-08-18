from flask import Flask, request
import requests
import json
import os
from datetime import datetime
import threading
import time

from ..config.constants import TOKEN_FILE, AUTH_URL
from ..config.constants_secure import CLIENT_SECRET, CLIENT_ID

class OneShotAuthServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.server_thread = None
        self.shutdown_event = threading.Event()
        self.token_recieved = False

        self.app.route('/exchange_token')(self.exchange_token)
        self.app.route('/health')(self.health_check)

    def exchange_token(self):
        """Handle the OAuth callback from Strava"""
        code = request.args.get('code')
        if not code:
            return 'No code provided', 400
        
        token_url = 'https://www.strava.com/oauth/token'
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }

        try:
            res = requests.post(token_url, data=payload)
            if res.status_code != 200:
                return f'Error: {res.status_code} - {res.text}', 500
            
            token_data = res.json()
            self.save_token(token_data)
            self.token_recieved = True

            self.shutdown_event.set()

            return """
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h2 style="color: green;">✅ Authentication Successful!</h2>
                <p>Your Strava token has been saved.</p>
                <p>You can close this window and return to your terminal.</p>
                <p style="color: gray; font-size: 12px;">This window will close automatically in 5 seconds...</p>
                <script>
                    setTimeout(function() { window.close(); }, 5000);
                </script>
            </body>
            </html>
            """
        
        except Exception as e:
            return f'Error: {str(e)}', 500

        
    def health_check(self):
        """Health check endpoint"""
        return 'OK', 200
        
    def save_token(self, token_data):
        """Save token to a JSON file"""
        token_data['saved_at'] = datetime.now().isoformat()
        with open(TOKEN_FILE, 'w') as f:
            json.dump(token_data, f, indent=2)
        print(f"Token saved to {TOKEN_FILE}")

    def start_server(self, port=3001):
        """Start the server in a seperate thread"""
        def run_server():
            self.app.run(port=port, debug=False, use_reloader=False)
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

        time.sleep(1)

        try:
            import requests
            response = requests.get(f'http://localhost:{port}/health', timeout=2)
            if response.status_code == 200:
                print(f"Auth server started on port {port}")
                return True
        except:
            pass

        print(f"Failed to start auth server on port {port}")
        return False
    
    def wait_for_token(self, timeout=300):
        """Wait for token to be received or timeout"""
        print("Waiting for Strava authorization...")

        if self.shutdown_event.wait(timeout):
            if self.token_recieved:
                print("Token received successfully")
                return True
            else:
                print("Server shutdown without recieving token")
                return False
        else:
            print("Timeout waiting for authorization")
            return False
        
    def stop_server(self):
        """Stop the server"""
        if self.server_thread and self.server_thread.is_alive():
            print("Auth server stopping")
            return True
        return False
    
def create_auth_server():
    """Factory function to create an auth server instance"""
    return OneShotAuthServer()

app = Flask(__name__)
