import pymongo
from datetime import datetime

mongodb_username = ''
mongodb_password = ''

uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}" + \
      "@seng3011-bobby-tables.q2umd.mongodb.net/api?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client.api

latest_scraper_version = db.articles.find_one({}, sort=[("scraper_version", pymongo.DESCENDING)])['scraper_version']


def filter_articles(end_date: datetime, start_date: datetime, key_terms: list, location: str, limit: int = 20,
                    offset: int = 0):
    cursor = db.articles.find({
        'scraper_version': latest_scraper_version,
        'date_of_publication': {'$lte': end_date, '$gte': start_date},
        'search_terms': {"$in": key_terms},
        'locations': {"$in": [location]}
    }).skip(offset).limit(limit)
    return list(cursor)
