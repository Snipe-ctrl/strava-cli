from typing import List
import requests

from .strava_api import get_headers
from ..config.constants import STRAVA_API_BASE, BROOKS_GHOST_DATE
from ..auth.strava_auth import load_token

def fetch_activities_page(*, after: int, page: int, per_page: int, base_url: str = STRAVA_API_BASE) -> List[dict]:
    url = f"{base_url}/athlete/activities"
    headers = get_headers(load_token())
    params = {"after": after, "page": page, "per_page": per_page}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        if resp.status_code != 200:
            return []
        return resp.json()
    except requests.RequestException:
        return []

def fetch_all_activities(*, after: int = BROOKS_GHOST_DATE, per_page: int = 200, base_url: str = STRAVA_API_BASE) -> List[dict]:
    page = 1
    out: List[dict] = []
    while True:
        batch = fetch_activities_page(after=after, page=page, per_page=per_page, base_url=base_url)
        if not batch:
            break
        out.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
    return out

def compute_total_miles() -> float:
    """Fetch total miles on Brooks Ghost shoes."""
    activities = fetch_all_activities(after=BROOKS_GHOST_DATE, per_page=200)
    total_miles = 0.0
    for a in activities:
        # Strava can use 'sport_type' on newer payloads; fall back to 'type'
        sport = a.get("sport_type") or a.get("type")
        distance = a.get("distance", 0) or 0
        if distance > 0 and sport == "Run":
            total_miles += meters_to_miles(distance)
    return total_miles

def meters_to_miles(meters):
    miles = meters / 1609.344
    return miles