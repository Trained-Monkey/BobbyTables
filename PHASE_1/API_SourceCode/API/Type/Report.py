from pydantic import BaseModel
from Type.Location import Location
from typing import List


class Report(BaseModel):
    diseases: : List[str]
    syndromes: List[str]
    event_date: str
    locations: List[Location]

    class Config:
        schema_extra = {
            'example': {
                "event_date": "2020-01-03 xx:xx:xx to 2020-01-15",
                "locations": [
                    {
                        "country": "China",
                        "location": "Wuhan, Hubei Province"
                    },
                    {
                        "country": "Japan",
                        "location": ""
                    }
                ],
                "diseases": [
                    "2019-nCoV"
                ],
                "syndromes": [
                    "Fever of unknown Origin"
                ]
            }
        }


class ReportList(BaseModel):
    reports: List[Report]
