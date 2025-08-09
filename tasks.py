from celery import Celery
from app.settings import get_settings
import logging

settings = get_settings()
celery_app = Celery("tn_tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@celery_app.task
def hello():
    logging.info("Celery is alive")


from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Alert, Job
from app.search import search_jobs

@celery_app.on_after_configure.connect
def setup_periodic(sender, **kwargs):
    # Every day at 09:00 UTC (adjust as needed)
    sender.add_periodic_task(24*60*60, daily_alerts.s(), name="daily_alerts")

@celery_app.task
def daily_alerts():
    db: Session = SessionLocal()
    try:
        alerts = db.execute(select(Alert)).scalars().all()
        for al in alerts:
            total, items = search_jobs(
                db,
                q=al.q, state=al.state, specialty=al.specialty,
                min_weekly=al.min_weekly, shift=al.shift, agency=al.agency,
                sort="-created_at", page=1, page_size=50
            )
            # Here you'd send email/push. We just log.
            print(f"[ALERT] to={'email:'+al.email if al.email else 'device:'+str(al.device_token)} found {total} matches")
    finally:
        db.close()


from app.sources import run_all, REGISTRY
import asyncio

@celery_app.task
def ingest_all():
    return asyncio.run(run_all())

@celery_app.task
def ingest_source(name: str):
    from app.sources import REGISTRY
    import asyncio
    if name not in REGISTRY:
        return f"unknown source {name}"
    from app.ingest import run_connector
    return asyncio.run(run_connector(REGISTRY[name], name))

@celery_app.on_after_configure.connect
def schedule_ingest(sender, **kwargs):
    # Stagger sources hourly; full run nightly
    hour = 0
    for name in REGISTRY.keys():
        sender.add_periodic_task(60*60, ingest_source.s(name), name=f"ingest_{name}")
        hour += 1
    # Full nightly at 03:00 UTC
    sender.add_periodic_task(24*60*60, ingest_all.s(), name="ingest_all_nightly")
