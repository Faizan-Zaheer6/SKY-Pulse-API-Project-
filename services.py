import os
import httpx
from fastapi import HTTPException

async def fetch_weather(city: str):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching weather data")
        
        data = response.json()
        return {
            "city": data["name"],
            "temperature": f"{data['main']['temp']}°C",
            "condition": data["weather"][0]["description"],
            "humidity": f"{data['main']['humidity']}%",
            "wind_speed": f"{data['wind']['speed']} m/s"
        }