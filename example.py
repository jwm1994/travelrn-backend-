# Skeleton for agency/site-specific crawlers.
# Each crawler should implement: fetch() -> list[dict]
# and map fields into the Job model shape.

import httpx
from bs4 import BeautifulSoup
from hashlib import sha256

async def fetch_example():
    # Example placeholder: Replace with real partner API or RSS if available.
    async with httpx.AsyncClient(timeout=30) as client:
        # url = "https://example.com/jobs/feed"
        # r = await client.get(url)
        # soup = BeautifulSoup(r.text, "lxml")
        return []
