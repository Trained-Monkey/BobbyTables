from pydantic import BaseModel
from Type.Location import Location

class Report(BaseModel):
    diseases: list[str]
    syndromes: str
    event_date: str
    locations: list[Location]
