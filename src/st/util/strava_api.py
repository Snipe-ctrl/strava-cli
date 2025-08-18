
def get_headers(token_data):
    """Get headers with authorization token"""
    return {
        'Authorization': f"Bearer {token_data['access_token']}"
    }