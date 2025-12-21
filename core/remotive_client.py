from typing import Any

import requests

BASE_URL = "https://remotive.com/api/remote-jobs"


from typing import Optional, List, Dict, Any

def fetch_jobs(search: Optional[str] = None) -> List[Dict[str, Any]]:

    params: dict[str, str] = {}
    if search:
        params["search"] = search

    r = requests.get(BASE_URL, params=params, timeout=30)
    r.raise_for_status()

    data = r.json()
    jobs = data.get("jobs", [])
    if not isinstance(jobs, list):
        return []

    return jobs
