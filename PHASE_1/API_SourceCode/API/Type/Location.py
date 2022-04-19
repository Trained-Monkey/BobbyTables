from pydantic import BaseModel

class Location(BaseModel):
    country: str
    location: str
    lat: float = None
    lng: float = None

    class Config:
        schema_extra = {
            'example': {
                "country": "China",
                "location": "Wuhan, Hubei Province",
                "lat": 30.596069,
                "lng": 114.297691
            }
        }