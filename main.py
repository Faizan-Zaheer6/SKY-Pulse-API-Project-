import os
from dotenv import load_dotenv
import httpx
import asyncio
from fastapi import FastAPI, Header, HTTPException
from schemas import WeatherResponse, ForecastDay

# 1. .env file se variables load karna
load_dotenv()

app = FastAPI()

# 2. Secrets ko environment se uthana (Hardcoding khatam)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
SECURITY_TOKEN = os.getenv("AUTH_TOKEN")

@app.get("/weather/{city_name}", response_model=WeatherResponse)
async def get_weather(city_name: str, x_auth_token: str = Header(None)):
    # Security Validation
    if x_auth_token != SECURITY_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Auth Token")

    async with httpx.AsyncClient() as client:
        # A. Geocoding: City name se coordinates lena
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={OPENWEATHER_API_KEY}"
        geo_res = await client.get(geo_url)
        geo_data = geo_res.json()

        # 🔥 Error Handling: Agar list khali [] hai toh crash na ho
        if not geo_data:
            raise HTTPException(status_code=404, detail=f"Location '{city_name}' not found!")
        
        lat, lon = geo_data[0]['lat'], geo_data[0]['lon']

        # B. Parallel API Calls: Weather aur Air Quality aik sath
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        
        w_res, a_res = await asyncio.gather(client.get(weather_url), client.get(aqi_url))
        
        # Check if calls were successful
        if w_res.status_code != 200:
            raise HTTPException(status_code=w_res.status_code, detail="Weather API error")

        w_data = w_res.json()
        a_data = a_res.json()

        # C. Forecast Trend Generation
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        mock_forecast = [
            ForecastDay(day=d, temp=round(w_data['main']['temp'] + i, 1), condition="Clear") 
            for i, d in enumerate(days)
        ]

        return {
            "city": city_name,
            "temperature": w_data['main']['temp'],
            "humidity": w_data['main']['humidity'],
            "wind_speed": w_data['wind']['speed'],
            "condition": w_data['weather'][0]['description'].capitalize(),
            "aqi": a_data['list'][0]['main']['aqi'] * 20, 
            "forecast": mock_forecast
        }