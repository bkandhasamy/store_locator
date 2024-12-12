from pydantic import BaseModel, condecimal
from datetime import time


class LocationCreate(BaseModel):
    id: int
    latitude: float
    longitude: float
    availability_radius: float
    open_hour: time
    close_hour: time
    rating: condecimal(gt=0, le=5, decimal_places=1)


class LocationRead(BaseModel):
    id: int
    latitude: float
    longitude: float
    availability_radius: float
    open_hour: time
    close_hour: time
    rating: float

    class Config:
        orm_mode = True
