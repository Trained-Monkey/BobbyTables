from pydantic import BaseModel

class Location(BaseModel):
    country: str
    location: str

    class Config:
        schema_extra = {
            'example': {
               "country": "China",
               "location": "Wuhan, Hubei Province"
            }
        }