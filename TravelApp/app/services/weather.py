
from datetime import date
from app.model import WeatherResponseModel
import httpx
from app.config import WEATHER_API_KEY
from app.services.cache import get_cache, set_cache

async def fetch_weather(
        destination:str,
        start_date:date,
        end_date:date,
) ->list[WeatherResponseModel]:

    cache_key= f"{destination}_{start_date}_{end_date}"
    cached_data = get_cache(cache_key)

    if cached_data:
        return cached_data
    

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.weatherapi.com/v1/forecast.json",
            params={
                "key": WEATHER_API_KEY,
                "q": destination,
                "dt": start_date,
                "end_dt": end_date,
            }
        )

    response.raise_for_status()
    data = response.json()

    forcasts=[]

    for day in data['forecast']['forecastday']:
        forcast = WeatherResponseModel(
            date=day['date'],
            condition=day['day']['condition']['text'],
            temp_high=day['day']['maxtemp_c'],
            temp_low=day['day']['mintemp_c'],
            humidity=day['day']['avghumidity'],
            rain_chance=day['day']['daily_chance_of_rain']
        )
        forcasts.append(forcast)  
        
    set_cache(cache_key, forcasts, 3600)  
    return forcasts