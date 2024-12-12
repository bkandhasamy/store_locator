import os
import aiohttp
import asyncio
import logging

from store_locator.database import SessionLocal
from store_locator.crud import create_location
from store_locator.schemas import LocationCreate
from sqlalchemy.orm import Session
from sqlalchemy import text
from store_locator.utils import logger


logging.getLogger(__name__)


async def schedule_data_loading():
    """This function loads the data for every six hours"""
    db = SessionLocal()
    while True:
        # Truncate table before load
        db.execute(text("TRUNCATE TABLE locations"))
        db.commit()
        logger.info("Data Loading in progress..")
        await fetch_csv_and_load(db)
        logger.info("Data Load Complete.")
        # Sleep for 6 hours
        await asyncio.sleep(6 * 3600)


# TODO - Load data in batch using generator
async def fetch_csv_and_load(db: Session):
    async with aiohttp.ClientSession() as session:
        async with session.get(os.getenv("CSV_URL")) as response:
            content = await response.text()
            rows = content.splitlines()
            for row in rows[1:]:  # Skip header
                fields = row.split(",")
                location = LocationCreate(
                    id=int(fields[0]),
                    latitude=float(fields[1]),
                    longitude=float(fields[2]),
                    availability_radius=float(fields[3]),
                    open_hour=fields[4],
                    close_hour=fields[5],
                    rating=float(fields[6]),
                )
                create_location(db, location)
