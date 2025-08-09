from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.db import get_db
from app.models import Alert, Job
from app.schemas import AlertIn, AlertOut
from app.search import search_jobs

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.post("", response_model=AlertOut)
def create_alert(payload: AlertIn, db: Session = Depends(get_db)):
    if not payload.email and not payload.device_token:
        raise HTTPException(400, "Provide email or device_token")
    alert = Alert(
        email=payload.email,
        device_token=payload.device_token,
        q=payload.q,
        state=(payload.state.upper() if payload.state else None),
        specialty=payload.specialty,
        min_weekly=payload.min_weekly,
        shift=payload.shift,
        agency=payload.agency,
    )
    db.add(alert); db.commit(); db.refresh(alert)
    return alert

@router.get("", response_model=List[AlertOut])
def list_alerts(db: Session = Depends(get_db)):
    return db.execute(select(Alert).order_by(Alert.created_at.desc())).scalars().all()

@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(404, "Not found")
    db.delete(alert); db.commit()
    return {"status":"deleted"}
