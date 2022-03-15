from pydantic import BaseModel
from Type.Report import Report
from typing import List

class Article(BaseModel):
    url: str
    date_of_publication: str
    headline: str
    main_text: str
    reports: List[Report]