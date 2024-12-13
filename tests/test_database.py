import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from fastapi.testclient import TestClient
from database import init_db
from main import app
from models import Weather
from weather_service import fetch_weather_from_api
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

# Initialize the test client
client = TestClient(app)


@pytest.fixture(scope="module")
async def db_setup():
    # Test uchun in-memory SQLite bazasini yaratish
    init_db(app, test=True)
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    await Tortoise.init(
        db_url=f"postgres://{db_user}:{db_password}@{db_host}/{db_name}",  # Test uchun bazani in-memory qilamiz
        modules={"models": ["models"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

@pytest.mark.asyncio
async def test_db_connection():
    # Initialize database connection (for testing purposes)
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")

    await Tortoise.init(
        db_url=f"postgres://{db_user}:{db_password}@{db_host}/{db_name}",  # Use test DB credentials
        modules={"models": ["models"]},
    )
    await Tortoise.generate_schemas()  # Generate schemas for testing
    assert Tortoise._connections  # Ensure that the database connection is active
    await Tortoise.close_connections()  # Close connections after test

@pytest.mark.asyncio
async def test_create_weather_entry(db_setup):
    weather = await Weather.create(
        city="Tashkent",
        temperature=30.0,
        description="Clear",
        humidity=60,
        wind_speed=5.0,
        sunrise="2024-12-13 06:00:00",
        sunset="2024-12-13 18:00:00",
    )
    assert weather.city == "Tashkent"

@pytest.mark.asyncio
async def test_read_weather_entry():
    # Test reading a weather entry from the database
    weather_data = {
        "city": "Tashkent",
        "temperature": 30.5,
        "description": "Clear sky",
        "humidity": 45,
        "wind_speed": 3.5,
        "sunrise": datetime.utcnow(),
        "sunset": datetime.utcnow(),
    }

    # Create a new weather entry
    weather_entry = await Weather.create(**weather_data)

    # Fetch the created weather entry by ID
    fetched_entry = await Weather.get(id=weather_entry.id)

    # Verify the fetched data matches the created entry
    assert fetched_entry.city == weather_data["city"]
    assert fetched_entry.temperature == weather_data["temperature"]
    assert fetched_entry.description == weather_data["description"]

@pytest.mark.asyncio
async def test_update_weather_entry():
    # Test updating an existing weather entry
    weather_data = {
        "city": "Tashkent",
        "temperature": 30.5,
        "description": "Clear sky",
        "humidity": 45,
        "wind_speed": 3.5,
        "sunrise": datetime.utcnow(),
        "sunset": datetime.utcnow(),
    }

    # Create a new weather entry
    weather_entry = await Weather.create(**weather_data)

    # Update the weather entry
    weather_entry.temperature = 32.0
    weather_entry.description = "Partly cloudy"
    await weather_entry.save()

    # Fetch the updated entry and verify changes
    updated_entry = await Weather.get(id=weather_entry.id)
    assert updated_entry.temperature == 32.0
    assert updated_entry.description == "Partly cloudy"

@pytest.mark.asyncio
async def test_delete_weather_entry():
    # Test deleting a weather entry
    weather_data = {
        "city": "Tashkent",
        "temperature": 30.5,
        "description": "Clear sky",
        "humidity": 45,
        "wind_speed": 3.5,
        "sunrise": datetime.utcnow(),
        "sunset": datetime.utcnow(),
    }

    # Create a new weather entry
    weather_entry = await Weather.create(**weather_data)

    # Delete the weather entry
    await weather_entry.delete()

    # Verify that the entry no longer exists
    with pytest.raises(Weather.DoesNotExist):
        await Weather.get(id=weather_entry.id)

@pytest.mark.asyncio
async def test_weather_data_in_api():
    # Test if the weather data in the API matches the database
    weather_data = {
        "city": "Tashkent",
        "temperature": 30.5,
        "description": "Clear sky",
        "humidity": 45,
        "wind_speed": 3.5,
        "sunrise": datetime.utcnow(),
        "sunset": datetime.utcnow(),
    }

    # Create a new weather entry in the database
    weather_entry = await Weather.create(**weather_data)

    # Make an API request to fetch weather for Tashkent
    response = client.get("/weather?city=Tashkent")
    assert response.status_code == 200
    data = response.json()

    # Verify that the API data matches the database data
    assert data["city"] == weather_entry.city
    assert data["temperature"] == weather_entry.temperature
    assert data["description"] == weather_entry.description
