import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_weather_details():
    response = client.get("/weather/details/?city=Tashkent")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert "temperature" in data
    assert "humidity" in data
    assert "wind_speed" in data
    assert "sunrise" in data
    assert "sunset" in data
