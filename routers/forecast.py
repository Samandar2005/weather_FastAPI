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
