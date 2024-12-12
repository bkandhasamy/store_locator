from sqlalchemy import Column, Float, Integer, Time, CheckConstraint, Index
from store_locator.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    availability_radius = Column(Float, nullable=False)
    open_hour = Column(Time, nullable=False)
    close_hour = Column(Time, nullable=False)
    rating = Column(Float, nullable=False)

    # Adding constraints to ensure data consistency
    __table_args__ = (
        CheckConstraint(
            "latitude >= -90 AND latitude <= 90", name="check_latitude"
        ),
        CheckConstraint(
            "longitude >= -180 AND longitude <= 180", name="check_longitude"
        ),
        CheckConstraint(
            "availability_radius > 0", name="check_availability_radius_positive"
        ),
        CheckConstraint(
            "rating >= 1 AND rating <= 5", name="check_rating_range"
        ),
        Index("ix_location_coordinates", "latitude", "longitude"),
    )
