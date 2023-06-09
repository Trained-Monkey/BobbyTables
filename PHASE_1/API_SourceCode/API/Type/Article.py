from pydantic import BaseModel
from Type.Report import Report
from typing import List


class Article(BaseModel):
    url: str
    date_of_publication: str
    headline: str
    main_text: str
    reports: List[Report]

    class Config:
        schema_extra = {
            "example": {
                "url": "https://www.who.int/csr/don/17-january-2020-novel-coronavirus-japan-ex-china/en/",
                "date_of_publication": "A very nice Item",
                "headline": "Novel Coronavirus – Japan (ex-China)",
                "main_text": "On 15 January 2020, the Ministry of Health, Labour and Welfare, Japan (MHLW) reported an imported case of laboratory-confirmed 2019-novel coronavirus (2019-nCoV) from Wuhan, Hubei Province, China. The case-patient is male, between the age of 30-39 years, living in Japan. The case-patient travelled to Wuhan, China in late December and developed fever on 3 January 2020 while staying in Wuhan. He did not visit the Huanan Seafood Wholesale Market or any other live animal markets in Wuhan. He has indicated that he was in close contact with a person with pneumonia. On 6 January, he traveled back to Japan and tested negative for influenza when he visited a local clinic on the same day.",
                "reports": [
                    {
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
                    }]
            }
        }

class ArticleIDPair(BaseModel):
    article: Article
    articleId: int

class ArticleList(BaseModel):
    articles: List[ArticleIDPair]
    max_articles: int
