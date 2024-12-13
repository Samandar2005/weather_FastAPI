import requests
from datetime import datetime, timedelta

API_KEY = "1434fabfe549dd24235b6ab10f99b1ac"
BASE_URL = "https://api.openweathermap.org/data/2.5/"

def format_time(timestamp: int, timezone_offset: int) -> str:
    utc_time = datetime.utcfromtimestamp(timestamp)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime("%Y-%m-%d %H:%M:%S")

def fetch_weather_from_api(city: str):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL + "weather", params=params)
    response.raise_for_status()
    return response.json()

def fetch_forecast_from_api(city: str, endpoint: str):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL + endpoint, params=params)
    response.raise_for_status()
    return response.json()
