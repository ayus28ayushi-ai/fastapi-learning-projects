from fastapi import APIRouter, HTTPException
from app.model import TravelRequestModel
from fastapi.responses import StreamingResponse
import json
from fastapi.encoders import jsonable_encoder # we are using this to convert the pydantic models to dict/list first
from app.services.weather import fetch_weather
from app.services.place import fetch_places
from app.services.currency import fetch_currency

router = APIRouter(
    prefix="/stream",
    tags=["stream"]
)

# helper function to 
def format_sse(data: str, event:str = None)->str:
    raw_data = jsonable_encoder(data) # converta the pydantic model to dict/list
    json_data = json.dumps(raw_data)  # converts the dict/list to raw json string
    return  f"data: {json_data}\n\n" if event is None else f"event: {event}\ndata: {data}\n\n"

async def stream_generator(req: TravelRequestModel):
    yield format_sse({"message": "Starting Travel Plan Aggregation"}, event="start")
    yield format_sse({"message": "Fetching weather data"}, event="weather")
    weather_data = await fetch_weather(
                destination=req.destination, 
                start_date=req.start_date, 
                end_date=req.end_date
                )
    yield format_sse({"weather": weather_data}, event="weather completed")
    yield format_sse({"message": "Fetching places data"}, event="places")
    places_data = await fetch_places(req.destination)
    yield format_sse({"places": places_data}, event="places completed")
    yield format_sse({"message": "Fetching currency data"}, event="currency")
    currency_data = await fetch_currency(req.base_currency)
    yield format_sse({"currency": currency_data}, event="currency completed")
    yield format_sse({"message": "Travel Plan aggregation completed!"}, event="complete")

@router.post("/plan", response_class=StreamingResponse)
async def stream_travel_plan(req: TravelRequestModel):
    # exception handling for invalid dates
    if req.start_date > req.end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date")

    trip_days = (req.end_date - req.start_date).days
    if trip_days > 14:
        raise HTTPException(status_code=400, detail="Trip duration cannot exceed 14 days")
    if trip_days < 1:
        raise HTTPException(status_code=400, detail="Trip duration must be at least 1 day")

    return StreamingResponse(
        stream_generator(req),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )