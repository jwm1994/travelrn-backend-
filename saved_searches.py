from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.db import get_db
from app.models import SavedSearch
from app.schemas import SavedSearchIn, SavedSearchOut

router = APIRouter(prefix="/saved-searches", tags=["saved-searches"])

@router.post("", response_model=SavedSearchOut)
def create_saved(payload: SavedSearchIn, db: Session = Depends(get_db)):
    if not payload.name:
        raise HTTPException(400, "Name required")
    s = SavedSearch(
        name=payload.name,
        email=payload.email,
        device_token=payload.device_token,
        q=payload.q,
        state=(payload.state.upper() if payload.state else None),
        specialty=payload.specialty,
        min_weekly=payload.min_weekly,
        shift=payload.shift,
        agency=payload.agency,
    )
    db.add(s); db.commit(); db.refresh(s)
    return s

@router.get("", response_model=List[SavedSearchOut])
def list_saved(db: Session = Depends(get_db)):
    return db.execute(select(SavedSearch).order_by(SavedSearch.created_at.desc())).scalars().all()

@router.delete("/{sid}")
def delete_saved(sid: int, db: Session = Depends(get_db)):
    s = db.get(SavedSearch, sid)
    if not s:
        raise HTTPException(404, "Not found")
    db.delete(s); db.commit()
    return {"status":"deleted"}
