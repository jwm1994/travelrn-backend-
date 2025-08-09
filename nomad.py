import os, httpx, asyncio
from datetime import date

API_URL = os.getenv("NOMAD_API_URL", "")
API_KEY = os.getenv("NOMAD_API_KEY", "")

async def fetch():
    # If partner API is available, implement actual calls here.
    # Placeholder returns empty list unless a test URL is set.
    if not API_URL:
        return []

    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(API_URL, headers=headers)
        r.raise_for_status()
        data = r.json()
        # Map partner fields → normalized fields
        items = []
        for x in data.get("jobs", []):
            items.append({
                "title": x.get("title",""),
                "specialty": x.get("specialty",""),
                "location_city": x.get("city",""),
                "location_state": x.get("state",""),
                "pay_weekly": x.get("pay_weekly"),
                "shift": x.get("shift"),
                "contract_weeks": x.get("weeks"),
                "agency": "Nomad",
                "hospital": x.get("hospital"),
                "start_date": x.get("start_date"),
                "url": x.get("apply_url") or x.get("url"),
                "latitude": x.get("lat"),
                "longitude": x.get("lon"),
            })
        return items
