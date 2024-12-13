import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_weather():
    response = client.get("/weather?city=Tashkent")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert "temperature" in data
    assert "description" in data


def test_weather_not_found():
    response = client.get("/weather?city=NonExistentCity")
    assert response.status_code == 404
