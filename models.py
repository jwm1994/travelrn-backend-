from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base
from datetime import datetime

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    specialty: Mapped[str] = mapped_column(String(100), index=True)
    location_city: Mapped[str] = mapped_column(String(100), index=True)
    location_state: Mapped[str] = mapped_column(String(2), index=True)
    pay_hourly: Mapped[float | None] = mapped_column(Float, nullable=True)
    pay_weekly: Mapped[float | None] = mapped_column(Float, nullable=True)
    agency: Mapped[str] = mapped_column(String(120), index=True)
    hospital: Mapped[str | None] = mapped_column(String(200), nullable=True)
    start_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    shift: Mapped[str | None] = mapped_column(String(50), nullable=True)  # e.g., "3x12 Nights"
    contract_weeks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    url: Mapped[str] = mapped_column(Text, unique=True)
    source: Mapped[str] = mapped_column(String(120), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True, index=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    hash: Mapped[str] = mapped_column(String(64), index=True)  # for dedupe


class Alert(Base):
    __tablename__ = "alerts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    # User contact: choose email OR device token for push, we'll just store as text for now
    email: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
    device_token: Mapped[str | None] = mapped_column(String(300), nullable=True, index=True)

    # Filters snapshot
    q: Mapped[str | None] = mapped_column(String(200), nullable=True)
    state: Mapped[str | None] = mapped_column(String(2), nullable=True, index=True)
    specialty: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    min_weekly: Mapped[float | None] = mapped_column(Float, nullable=True, index=True)
    shift: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    agency: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)

    # For dedupe per run: remember last job id seen
    last_seen_job_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)


class SavedSearch(Base):
    __tablename__ = "saved_searches"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
    device_token: Mapped[str | None] = mapped_column(String(300), nullable=True, index=True)
    q: Mapped[str | None] = mapped_column(String(200), nullable=True)
    state: Mapped[str | None] = mapped_column(String(2), nullable=True, index=True)
    specialty: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    min_weekly: Mapped[float | None] = mapped_column(Float, nullable=True, index=True)
    shift: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    agency: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)


class Device(Base):
    __tablename__ = "devices"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    platform: Mapped[str] = mapped_column(String(20), index=True)  # 'ios' or 'android'
    token: Mapped[str] = mapped_column(String(300), unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
