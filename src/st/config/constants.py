
from pathlib import Path
import os

APP_DIR = Path(os.getenv("ST_APP_DIR", Path.home() / ".st"))
TOKEN_FILE = Path(os.getenv("ST_TOKEN_FILE", APP_DIR / "strava_token.json"))

#auth/general constants
AUTH_URL = "https://www.strava.com/oauth/authorize?client_id=171735&response_type=code&redirect_uri=http://localhost:3001/exchange_token&approval_prompt=force&scope=read,activity:read"

#strava api
STRAVA_API_BASE = 'https://www.strava.com/api/v3'

#shoe constants
BROOKS_GHOST_DATE = '1732372500'
BROOKS_GHOST_ID = '12968521025'