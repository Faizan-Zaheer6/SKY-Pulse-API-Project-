from pydantic import BaseModel
from typing import List

# Weather Forecast Model
class ForecastDay(BaseModel):
    day: str
    temp: float
    condition: str

# Main Weather Response Model
class WeatherResponse(BaseModel):
    city: str
    temperature: float
    humidity: int
    wind_speed: float
    condition: str
    aqi: int  # New Field for Air Quality
    forecast: List[ForecastDay]  # New Field for 7-Day Trend