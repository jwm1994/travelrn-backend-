import asyncio
import logging
from typing import List, Dict, Any, Callable, Awaitable
from hashlib import sha256
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Job
from app.geo import centroid

logger = logging.getLogger(__name__)

def stable_hash(fields: Dict[str, Any]) -> str:
    blob = "|".join(str(fields.get(k, "")) for k in ["title","specialty","location_city","location_state","pay_weekly","agency","hospital","start_date","url"])
    return sha256(blob.encode("utf-8")).hexdigest()

async def normalize_and_upsert(db: Session, records: List[Dict[str, Any]], source: str) -> int:
    created = 0
    for r in records:
        try:
            city = (r.get("location_city") or "").title()
            state = (r.get("location_state") or "").upper()
            lat, lon = (None, None)
            if city and state:
                c = centroid(city, state)
                if c: lat, lon = c
            fields = {
                "title": r.get("title","").strip(),
                "specialty": r.get("specialty","").strip(),
                "location_city": city,
                "location_state": state,
                "pay_hourly": r.get("pay_hourly"),
                "pay_weekly": r.get("pay_weekly"),
                "agency": r.get("agency","").strip() or source,
                "hospital": r.get("hospital"),
                "start_date": r.get("start_date"),
                "shift": r.get("shift"),
                "contract_weeks": r.get("contract_weeks"),
                "url": r.get("url"),
                "source": source,
                "latitude": r.get("latitude", lat),
                "longitude": r.get("longitude", lon),
            }
            h = stable_hash(fields)
            fields["hash"] = h

            # Check existing by url or hash
            existing = db.execute(select(Job).where(Job.url == fields["url"])).scalar_one_or_none()
            if existing is None:
                job = Job(**fields, created_at=datetime.utcnow())
                db.add(job); created += 1
            else:
                for k, v in fields.items():
                    setattr(existing, k, v)
        except Exception as e:
            logger.exception(f"Normalize failure for source={source}: {e}")
    db.commit()
    return created

async def run_connector(connector: Callable[[], Awaitable[List[Dict[str, Any]]]], source: str) -> int:
    db = SessionLocal()
    try:
        records = await connector()
        if not isinstance(records, list):
            logger.error(f"Connector {source} did not return list")
            return 0
        created = await normalize_and_upsert(db, records, source)
        logger.info(f"[INGEST] {source}: upserted {len(records)} (created {created})")
        return created
    finally:
        db.close()
