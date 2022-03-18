import pymongo
from datetime import datetime
from Type.Article import Article
from Type.Report import Report
from Type.Location import Location


mongodb_username = 'bobby'  # TODO: fill these in manually
mongodb_password = 'tables'

uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}" + \
      "@seng3011-bobby-tables.q2umd.mongodb.net/api?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client.api

latest_scraper_version = db.articles.find_one({}, sort=[("scraper_version", pymongo.DESCENDING)])['scraper_version']


def filter_articles(end_date: datetime, start_date: datetime, key_terms: list, location: str, limit: int = 20,
                    offset: int = 0):
    query = {
        'scraper_version': latest_scraper_version,
        'date_of_publication': {'$lte': end_date, '$gte': start_date},
    }
    if len(key_terms) > 0:
        query.update({'search_terms': {"$in": key_terms}})
    if len(location) > 0:
        query.update({'locations': {"$in": [location]}})
    cursor = db.articles.find(query).skip(offset).limit(limit)
    articles = []
    ids = []
    for dic in cursor:
        reports = []
        for report_dict in dic['reports']:
            locations = []
            for location_name in report_dict['locations']:
                location = Location(
                    country='',
                    location=location_name
                )
                locations.append(location)
            report = Report(
                diseases=report_dict['diseases'],
                syndromes=report_dict['syndromes'],
                event_date=report_dict['event-date'],
                locations=locations
            )
            reports.append(report)
        article = Article(
            url=dic['url'],
            date_of_publication=dic['date_of_publication'].strftime("%Y-%m-%dT%H:%M:%S"),
            headline=dic['headline'],
            main_text=dic['main_text'],
            reports=reports
        )
        articles.append(article)
        ids.append(dic['id'])
    max_amount = db.articles.count_documents(query)
    return articles, ids, max_amount
