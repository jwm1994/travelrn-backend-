import random, string
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from app.db import Base, engine, SessionLocal
from app.models import Job
from app.geo import centroid

SPECIALTIES = ["OR","ICU","ER","Cath Lab","L&D","PACU","Stepdown","Tele","Med-Surg"]
SHIFTS = ["3x12 Days","3x12 Nights","4x10 Days","Days","Nights"]
AGENCIES = ["Aya","AMN","Cross Country","Nomad","Medical Solutions","TotalMed","Fusion","Host","Atlas","Vivian"]
CITIES = [
    ("Austin","TX"),("Houston","TX"),("Dallas","TX"),("San Antonio","TX"),
    ("Phoenix","AZ"),("Denver","CO"),("Miami","FL"),("Atlanta","GA"),
    ("Chicago","IL"),("Indianapolis","IN"),("Detroit","MI"),("Minneapolis","MN"),
    ("St. Louis","MO"),("Charlotte","NC"),("Omaha","NE"),("Las Vegas","NV"),
    ("New York","NY"),("Columbus","OH"),("Portland","OR"),("Philadelphia","PA"),
    ("Nashville","TN"),("Seattle","WA")
]

def seed(n=300):
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        for i in range(n):
            title = random.choice(["RN","Travel RN","Registered Nurse"]) + " - " + random.choice(SPECIALTIES)
            specialty = random.choice(SPECIALTIES)
            (city, state) = random.choice(CITIES)
            pay_weekly = random.choice([2200,2400,2600,2800,3000,3200,3500,3800,4000])
            shift = random.choice(SHIFTS)
            weeks = random.choice([8,10,12,13,26])
            agency = random.choice(AGENCIES)
            start_date = date.today() + timedelta(days=random.randint(7,45))
            url = f"https://example.com/{agency.lower()}/{''.join(random.choices(string.ascii_lowercase+string.digits,k=10))}"
            latlon = centroid(city, state)
            job = Job(
                title=title,
                specialty=specialty,
                location_city=city,
                location_state=state,
                pay_hourly=None,
                pay_weekly=pay_weekly,
                agency=agency,
                hospital=None,
                start_date=start_date,
                shift=shift,
                contract_weeks=weeks,
                url=url,
                source=agency,
                created_at=datetime.utcnow(),
                hash=f"{agency}-{city}-{state}-{title}-{pay_weekly}",
                latitude=latlon[0] if latlon else None,
                longitude=latlon[1] if latlon else None
            )
            db.add(job)
        db.commit()
        print(f"Seeded {n} jobs.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
