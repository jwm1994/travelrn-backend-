from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List

class JobOut(BaseModel):
    id: int
    title: str
    specialty: str
    location_city: str
    location_state: str
    pay_hourly: Optional[float] = None
    pay_weekly: Optional[float] = None
    agency: str
    hospital: Optional[str] = None
    start_date: Optional[date] = None
    shift: Optional[str] = None
    contract_weeks: Optional[int] = None
    url: str
    source: str
    created_at: datetime
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True

class JobSearchResponse(BaseModel):
    total: int
    items: List[JobOut]


class AlertIn(BaseModel):
    email: Optional[str] = None
    device_token: Optional[str] = None
    q: Optional[str] = None
    state: Optional[str] = None
    specialty: Optional[str] = None
    min_weekly: Optional[float] = None
    shift: Optional[str] = None
    agency: Optional[str] = None

class AlertOut(BaseModel):
    id: int
    email: Optional[str] = None
    device_token: Optional[str] = None
    q: Optional[str] = None
    state: Optional[str] = None
    specialty: Optional[str] = None
    min_weekly: Optional[float] = None
    shift: Optional[str] = None
    agency: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True


class SavedSearchIn(BaseModel):
    name: str
    email: Optional[str] = None
    device_token: Optional[str] = None
    q: Optional[str] = None
    state: Optional[str] = None
    specialty: Optional[str] = None
    min_weekly: Optional[float] = None
    shift: Optional[str] = None
    agency: Optional[str] = None

class SavedSearchOut(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    device_token: Optional[str] = None
    q: Optional[str] = None
    state: Optional[str] = None
    specialty: Optional[str] = None
    min_weekly: Optional[float] = None
    shift: Optional[str] = None
    agency: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True


class DeviceIn(BaseModel):
    platform: str
    token: str
    email: Optional[str] = None

class DeviceOut(BaseModel):
    id: int
    platform: str
    token: str
    email: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True
