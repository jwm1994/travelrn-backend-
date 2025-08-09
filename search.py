from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import Optional, Tuple
from app.models import Job

def search_jobs(
    db: Session,
    q: Optional[str] = None,
    state: Optional[str] = None,
    specialty: Optional[str] = None,
    min_weekly: Optional[float] = None,
    shift: Optional[str] = None,
    agency: Optional[str] = None,
    sort: str = "-created_at",
    page: int = 1,
    page_size: int = 20,
) -> Tuple[int, list[Job]]:
    stmt = select(Job)
    filters = []
    if q:
        like = f"%{q.lower()}%"
        filters.append(and_(Job.title.ilike(like) | Job.hospital.ilike(like) | Job.location_city.ilike(like)))
    if state:
        filters.append(Job.location_state == state.upper())
    if specialty:
        filters.append(Job.specialty.ilike(f"%{specialty}%"))
    if min_weekly:
        filters.append(Job.pay_weekly >= float(min_weekly))
    if shift:
        filters.append(Job.shift.ilike(f"%{shift}%"))
    if agency:
        filters.append(Job.agency.ilike(f"%{agency}%"))

    if filters:
        stmt = stmt.where(and_(*filters))

    # Sorting
    if sort.startswith("-", user_lat: float | None = None, user_lon: float | None = None):
        order = getattr(Job, sort[1:], None).desc()
    else:
        order = getattr(Job, sort, None).asc()
    if order is not None:
        stmt = stmt.order_by(order)

    total = db.execute(select(Job).where(and_(*filters)) if filters else select(Job)).scalars().all()
    total_count = len(total)

    if sort == "distance" and user_lat is not None and user_lon is not None:
        # Fetch more rows for better client-side distance sorting
        items = db.execute(stmt.limit(page_size*5)).scalars().all()
        def hav(a,b,c,d):
            import math
            R=6371.0
            la1=math.radians(a); lo1=math.radians(b); la2=math.radians(c); lo2=math.radians(d)
            dlat=la2-la1; dlon=lo2-lo1
            h=math.sin(dlat/2)**2+math.cos(la1)*math.cos(la2)*math.sin(dlon/2)**2
            return 2*R*math.asin(math.sqrt(h))
        items = sorted(items, key=lambda j: 1e9 if j.latitude is None or j.longitude is None else hav(user_lat,user_lon,j.latitude,j.longitude))
        items = items[:page_size]
    else:
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        items = db.execute(stmt).scalars().all()
    return total_count, items

# search returns Job models including latitude/longitude if set
