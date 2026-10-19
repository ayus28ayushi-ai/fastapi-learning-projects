from fastapi import APIRouter, HTTPException
from app.model import TravelRequestModel
from app.services.weather import fetch_weather
from app.services.place import fetch_places
from app.services.currency import fetch_currency
import asyncio
from app.services.cache import clear_cache, get_all_cache
router = APIRouter(
    prefix="/plan", 
    tags=["Travel Plan"]
)

@router.post("/", summary="Create a travel plan", description="Aggregate travel data from multiple sources to provide a single plan")
async def create_travel_plan(travel_req: TravelRequestModel):

    # exception handling for invalid dates
    if travel_req.start_date > travel_req.end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date")

    trip_days = (travel_req.end_date - travel_req.start_date).days
    if trip_days > 14:
        raise HTTPException(status_code=400, detail="Trip duration cannot exceed 14 days")
    if trip_days < 1:
        raise HTTPException(status_code=400, detail="Trip duration must be at least 1 day")

    """ this way instead of having three awaits that was blocking , one would wait for the other to finish, 
        using this asyncio, we can run them together (in parallel) without them blocking each other
    """
   
    weather_data, places, currency_data = await asyncio.gather(
        fetch_weather(
            destination=travel_req.destination, 
            start_date=travel_req.start_date, 
            end_date=travel_req.end_date
            ),
        fetch_places(travel_req.destination),
        fetch_currency(travel_req.base_currency)
    )

    if not places:
        raise HTTPException(status_code=404, detail=f"No places found for {travel_req.destination}")
    
    if not currency_data:
        raise HTTPException(status_code=404, detail=f"No currency data found for {travel_req.base_currency}")
    
    return {
        "message": "Travel plan created successfully",
        "weather_data": weather_data,
        "places": places,
        "currency": currency_data
    }

@router.delete("/cache")
async def delete_cache():
    clear_cache()
    return {
        "message": "Cache cleared successfully",
        "cache": get_all_cache()
    }

@router.get("/cache-stats")
async def get_cache_stats():
    return get_all_cache()