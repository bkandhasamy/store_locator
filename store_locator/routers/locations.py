from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from store_locator.schemas import LocationCreate, LocationRead
from store_locator.crud import (
    create_location,
    get_location,
    get_locations,
    get_store_list,
)
from store_locator import query
from store_locator.database import get_db
from store_locator.utils import logger
from store_locator.exceptions import LocationNotFoundException


router = APIRouter(prefix="/locations", tags=["Locations"])


@router.post("/", response_model=LocationRead, status_code=201)
def create_new_location(
    location: LocationCreate, db: Session = Depends(get_db)
) -> LocationRead:
    """
    Create a new location.
    Args:
        location: LocationCreate schema containing location details.
        db: database local session

    Returns:
        Newly created location as LocationRead schema.
    """
    try:
        new_location = create_location(db, location)
        logger.info(f"Created new location: {new_location}")
        return new_location
    except Exception as e:
        logger.error(f"Error creating location: {e}")
        raise HTTPException(status_code=500, detail="Failed to create location")


@router.get("/{location_id}", response_model=LocationRead)
def read_location(
    location_id: int, db: Session = Depends(get_db)
) -> LocationRead:
    """
    Retrieve a location by its ID.
    Args:
        location_id: Unique identifier of the location.
        db: database local session

    Returns:
        The location as LocationRead schema.
    """
    try:
        location = get_location(db, location_id)
        if not location:
            logger.warning(f"Location not found: {location_id}")
            raise LocationNotFoundException(location_id)
        logger.info(f"Retrieved location: {location}")
        return location
    except LocationNotFoundException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving location {location_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch location")


@router.get("/", response_model=List[LocationRead])
def read_locations(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of records to retrieve"
    ),
    db: Session = Depends(get_db),
) -> List[LocationRead]:
    """
    Retrieve a list of locations with pagination.
    Args:
        skip: Number of records to skip (default is 0).
        limit: Maximum number of records to retrieve (default is 100, max is 1000).
        db: database local session

    Returns:
        List of locations as LocationRead schema.
    """
    try:
        locations = get_locations(db, skip=skip, limit=limit)
        logger.info(
            f"Retrieved {len(locations)} locations (skip={skip}, limit={limit})"
        )
        return locations
    except Exception as e:
        logger.error(f"Error fetching locations: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch locations")


@router.get("/coordinates/{coordinates}")
def get_stores(coordinates: str):
    latitude, longitude = coordinates.split("|")
    stores = get_store_list(
        query=query.stores, latitude=float(latitude), longitude=float(longitude)
    )
    return stores
