from fastapi import APIRouter, HTTPException
from app.model import TravelRequestModel
from app.services.weather import fetch_weather
from app.services.place import fetch_places

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
    
    weather_data = await fetch_weather(
        destination=travel_req.destination, 
        start_date=travel_req.start_date, 
        end_date=travel_req.end_date
    )

    places =  await fetch_places(travel_req.destination)

    if not places:
        raise HTTPException(status_code=404, detail=f"No places found for {travel_req.destination}")
    
    return {
        "message": "Travel plan created successfully",
        "weather_data": weather_data,
        "places": places
    }