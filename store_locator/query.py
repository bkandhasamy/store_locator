from sqlalchemy import text

stores = text(
f"""
SELECT id, availability_radius, open_hour, close_hour, rating 
FROM LOCATIONS
WHERE latitude = :latitude
AND longitude = :longitude
"""
)
