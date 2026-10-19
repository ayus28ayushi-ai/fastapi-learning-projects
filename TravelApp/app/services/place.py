from app.model import PlaceModel
from app.data.places import PLACES_DATABASE

async def fetch_places(destination: str) -> list[PlaceModel]:
    return PLACES_DATABASE.get(destination.lower(), [])