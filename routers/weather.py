from fastapi import APIRouter, HTTPException
from models import Weather
from schemas import WeatherResponse
from weather_service import fetch_weather_from_api, format_time
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=WeatherResponse)
async def get_weather(city: str):
    # Fetch from API
    data = fetch_weather_from_api(city)

    result = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "sunrise": format_time(data["sys"]["sunrise"], data["timezone"]),
        "sunset": format_time(data["sys"]["sunset"], data["timezone"]),
    }

    # Save to database
    await Weather.create(
        city=data["name"],
        temperature=data["main"]["temp"],
        description=data["weather"][0]["description"],
        humidity=data["main"]["humidity"],
        wind_speed=data["wind"]["speed"],
        sunrise=datetime.utcfromtimestamp(data["sys"]["sunrise"]),
        sunset=datetime.utcfromtimestamp(data["sys"]["sunset"]),
    )

    return result


@router.get("/details/", response_model=WeatherResponse)
async def get_weather_details(city: str):
    data = fetch_weather_from_api(city)

    result = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "sunrise": format_time(data["sys"]["sunrise"], data["timezone"]),
        "sunset": format_time(data["sys"]["sunset"], data["timezone"]),
    }

    return result


@router.get("/air_quality/", response_model=WeatherResponse)
async def get_air_quality(city: str):
    data = fetch_weather_from_api(city)
    air_quality = data.get("air_quality", {}).get("index", "N/A")

    result = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "air_quality_index": air_quality,
        "description": data["weather"][0]["description"],
    }

    return result
