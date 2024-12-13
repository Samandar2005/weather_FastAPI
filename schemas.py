from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    sunrise: str
    sunset: str


class ForecastResponse(BaseModel):
    city: str
    forecast: list
