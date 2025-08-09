from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
import orjson

from app.db import Base, engine, get_db
from app.schemas import JobSearchResponse, JobOut
from app.search import search_jobs
from app import alerts as alerts_router
from app import saved_searches as saved_router
from app import sources_api
from app import devices as devices_router

app = FastAPI(title="Travel Nurse Aggregator", default_response_class=None)

# CORS for local dev + iOS app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alerts_router.router)
app.include_router(saved_router.router)
app.include_router(sources_api.router)
app.include_router(devices_router.router)

# Create tables for dev
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/jobs", response_model=JobSearchResponse)
def jobs(
    q: Optional[str] = Query(None, description="Free text search"),
    state: Optional[str] = Query(None, min_length=2, max_length=2),
    specialty: Optional[str] = None,
    min_weekly: Optional[float] = None,
    shift: Optional[str] = None,
    agency: Optional[str] = None,
    sort: str = "-created_at",
    user_lat: float | None = Query(None),
    user_lon: float | None = Query(None),
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
):
    total, items = search_jobs(db, q=q, state=state, specialty=specialty, min_weekly=min_weekly,
                               shift=shift, agency=agency, sort=sort, page=page, page_size=page_size,
                               user_lat=user_lat, user_lon=user_lon)
    return {"total": total, "items": items}
