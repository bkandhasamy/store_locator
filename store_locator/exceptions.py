from fastapi import HTTPException


class StoreLocatorError(Exception):
    """Base exception to Store Locator"""


class LocationNotFoundException(HTTPException):
    """Custom exception for location not found"""

    def __init__(self, location_id: int):
        super().__init__(
            status_code=404,
            detail=f"Location with ID {location_id} not found.",
        )
