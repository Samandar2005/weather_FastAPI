from fastapi import FastAPI
from database import init_db
from routers import weather, forecast

app = FastAPI()

# Initialize database
init_db(app)

# Include routers
app.include_router(weather.router, prefix="/weather", tags=["Weather"])
app.include_router(forecast.router, prefix="/forecast", tags=["Forecast"])
