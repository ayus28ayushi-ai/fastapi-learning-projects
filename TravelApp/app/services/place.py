from app.model import PlaceModel
from app.data.places import PLACES_DATABASE

async def fetch_places(destination: str) -> list[PlaceModel]:
    query = destination.strip().lower()
    for city, places_list in PLACES_DATABASE.items():
        print(f"DEBUG: {city}")
        if city.strip().lower() == query:
            return places_list
    
    return []