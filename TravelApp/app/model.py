from pydantic import BaseModel
from datetime import date

class TravelRequestModel(BaseModel):
    destination: str
    start_date: date
    end_date: date
    base_currency: str = "INR"

class WeatherResponseModel(BaseModel):
    date: str
    condition:str
    temp_high: float
    temp_low: float
    humidity: float
    rain_chance: float

class PlaceModel(BaseModel):
    name: str
    description: str
    category: str
    rating: float
    estimated_time_hours: int