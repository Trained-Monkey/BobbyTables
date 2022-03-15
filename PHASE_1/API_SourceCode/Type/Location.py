from pydantic import BaseModel

class Location(BaseModel):
    country: str
    location: str