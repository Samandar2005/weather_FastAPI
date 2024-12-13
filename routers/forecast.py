from fastapi import APIRouter, HTTPException
from schemas import ForecastResponse
from weather_service import fetch_forecast_from_api, format_time

router = APIRouter()


@router.get("/hourly/", response_model=ForecastResponse)
async def get_hourly_forecast(city: str):
    data = fetch_forecast_from_api(city, "forecast")
    forecast = [
        {
            "time": format_time(item["dt"], data["city"]["timezone"]),
            "temperature": item["main"]["temp"],
            "description": item["weather"][0]["description"],
        }
        for item in data["list"][:8]
    ]
    return {"city": data["city"]["name"], "forecast": forecast}


@router.get("/hourly/{hours}", response_model=ForecastResponse)
async def get_custom_hourly_forecast(city: str, hours: int):
    data = fetch_forecast_from_api(city, "forecast")
    forecast = [
        {
            "time": format_time(item["dt"], data["city"]["timezone"]),
            "temperature": item["main"]["temp"],
            "description": item["weather"][0]["description"],
        }
        for item in data["list"][:hours]
    ]
    return {"city": data["city"]["name"], "forecast": forecast}


@router.get("/forecast/daily/", response_model=ForecastResponse)
async def get_daily_forecast(city: str):
    data = fetch_forecast_from_api(city, "onecall")
    forecast = [
        {
            "date": format_time(item["dt"], data["timezone_offset"]),
            "temperature": item["temp"]["day"],
            "description": item["weather"][0]["description"],
        }
        for item in data["daily"][:7]  # 7 kunlik prognoz
    ]
    return {"city": data["timezone"], "forecast": forecast}

