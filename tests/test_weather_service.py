import pytest
from weather_service import fetch_weather_from_api, fetch_forecast_from_api


def test_fetch_weather_from_api():
    data = fetch_weather_from_api("Tashkent")
    assert "main" in data
    assert "weather" in data
    assert "name" in data
    assert data["name"] == "Tashkent"


def test_fetch_forecast_from_api():
    data = fetch_forecast_from_api("Tashkent", "forecast")
    assert "list" in data
    assert len(data["list"]) > 0
