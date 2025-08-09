from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import get_db
from app.models import Device
from app.schemas import DeviceIn, DeviceOut

router = APIRouter(prefix="/devices", tags=["devices"])

@router.post("", response_model=DeviceOut)
def register_device(payload: DeviceIn, db: Session = Depends(get_db)):
    if payload.platform not in ("ios","android"):
        raise HTTPException(400, "platform must be 'ios' or 'android'")
    # Upsert by token
    existing = db.execute(select(Device).where(Device.token == payload.token)).scalar_one_or_none()
    if existing:
        existing.platform = payload.platform
        existing.email = payload.email
        db.commit(); db.refresh(existing)
        return existing
    d = Device(platform=payload.platform, token=payload.token, email=payload.email)
    db.add(d); db.commit(); db.refresh(d)
    return d
