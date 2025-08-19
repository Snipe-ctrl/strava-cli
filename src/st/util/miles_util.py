from typing import List
import requests
import time

from .strava_api import get_headers
from ..config.constants import STRAVA_API_BASE
from ..auth.strava_auth import load_token
from .shoe_util import meters_to_miles

def todays_date_epoch():
    today_epoch = int(time.time())
    return today_epoch

def fetch_activities_page_before_date(*, before: int, page: int, per_page: int, base_url: str = STRAVA_API_BASE) -> List[dict]:
    url = f"{base_url}/athlete/activities"
    headers = get_headers(load_token())
    params = {"before": before, "page": page, "per_page": per_page}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        if resp.status_code != 200:
            return []
        return resp.json()
    except requests.RequestException:
        return []
    
def fetch_all_runs(*, before: int = todays_date_epoch(), per_page: int = 200, base_url: str = STRAVA_API_BASE) -> List[dict]:
    page = 1
    out: List[dict] = []
    while True:
        batch = fetch_activities_page_before_date(before=before, page=page, per_page=per_page, base_url=base_url)
        if not batch:
            break
        out.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
    return out

def compute_total_miles() -> float:
    activities = fetch_all_runs(before=todays_date_epoch(), per_page=200)
    total_miles = 0.0
    for a in activities:
        sport = a.get("sport_type") or a.get("type")
        distance = a.get("distance", 0) or 0
        if distance > 0 and sport == "Run":
            total_miles += meters_to_miles(distance)
    return total_miles



    
