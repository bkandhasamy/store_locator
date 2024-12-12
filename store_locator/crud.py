import os
from sqlalchemy.orm import Session
from store_locator.models import Location
from store_locator.schemas import LocationCreate
from sqlalchemy.sql.elements import TextClause
from sqlalchemy import create_engine


def create_location(db: Session, location: LocationCreate):
    db_location = Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def get_location(db: Session, location_id: int):
    return db.query(Location).filter(Location.id == location_id).first()


def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Location).offset(skip).limit(limit).all()


def get_store_list(query: TextClause, latitude: float, longitude: float):
    engine = create_engine(os.getenv("DATABASE_URL"))
    with engine.connect() as connection:
        result = connection.execute(
            query, {"latitude": latitude, "longitude": longitude}
        ).fetchall()
    return [
        {
            "id": row[0],
            "availability_radius": row[1],
            "open_hour": row[2],
            "close_hour": row[3],
            "rating": row[4],
        }
        for row in result
    ]
