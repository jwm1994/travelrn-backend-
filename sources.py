from typing import Dict, Callable, Awaitable, List
import asyncio
import logging
from app.ingest import run_connector
from app.crawlers import aya, amn, cross_country, nomad, medical_solutions, totalmed, fusion, host, atlas, vivian

logger = logging.getLogger(__name__)

REGISTRY: Dict[str, Callable[[], Awaitable[List[dict]]]] = {
    "aya": aya.fetch,
    "amn": amn.fetch,
    "cross_country": cross_country.fetch,
    "nomad": nomad.fetch,
    "medical_solutions": medical_solutions.fetch,
    "totalmed": totalmed.fetch,
    "fusion": fusion.fetch,
    "host": host.fetch,
    "atlas": atlas.fetch,
    "vivian": vivian.fetch,
}

async def run_all() -> int:
    results = await asyncio.gather(*[run_connector(conn, name) for name, conn in REGISTRY.items()], return_exceptions=True)
    created_total = 0
    for name, res in zip(REGISTRY.keys(), results):
        if isinstance(res, Exception):
            logger.exception(f"{name} failed: {res}")
        else:
            created_total += int(res)
    return created_total
