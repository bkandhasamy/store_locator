import asyncio
from fastapi import FastAPI
from store_locator.database import init_db
from store_locator.loader import schedule_data_loading
from store_locator.routers import locations

app = FastAPI(title="Store Locator", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    await init_db()
    asyncio.create_task(schedule_data_loading())


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(locations.router)
