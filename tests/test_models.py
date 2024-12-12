import os
import time
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from store_locator.main import app
from store_locator.database import Base, get_db

load_dotenv()
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
# Setup a test database
if not TEST_DATABASE_URL:
    raise ValueError(f"Database url not set {TEST_DATABASE_URL}")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
# Base.metadata.create_all(bind=engine)


# Dependency override for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_benchmark_get_locations():
    """Test benchmark for get location"""
    start_time = time.time()
    response = client.get("/locations/")
    elapsed_time = time.time() - start_time
    assert response.status_code == 200
    assert elapsed_time < 0.2  # Ensure response is under 200ms


def test_create_location():
    """Test create location"""
    location_data = {
        "id": 0,
        "latitude": 51.1942536,
        "longitude": 6.455508,
        "availability_radius": 5,
        "open_hour": "14:00:00",
        "close_hour": "23:00:00",
        "rating": 4.7,
    }
    response = client.post("http://0.0.0.0:8000/locations", json=location_data)
    assert response.status_code == 201
    assert response.json()["id"] == 0
    assert response.json()["latitude"] == location_data["latitude"]
    assert response.json()["rating"] == location_data["rating"]


def test_get_location():
    """Test get location"""
    response = client.get("http://0.0.0.0:8000/locations/1")
    assert response.status_code == 200
    assert response.json()["latitude"] == 51.1942536
