import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_hourly_forecast():
    response = client.get("/forecast/hourly/?city=Tashkent")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert "forecast" in data
    assert len(data["forecast"]) > 0

def test_get_daily_forecast():
    response = client.get("/forecast/forecast/daily/?city=Tashkent")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert "forecast" in data
    assert len(data["forecast"]) > 0
