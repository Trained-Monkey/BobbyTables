import pymongo
from datetime import datetime
from Type.Article import Article
from Type.Report import Report, ReportList
from Type.Location import Location
from fastapi import HTTPException
from functools import wraps
import logging
import sys
import traceback

import os

mongodb_username = ''  # TODO: fill these in manually
mongodb_password = ''

uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}" + \
      "@seng3011-bobby-tables.q2umd.mongodb.net/api?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client.api

latest_scraper_version = db.articles.find_one({}, sort=[("scraper_version", pymongo.DESCENDING)])['scraper_version']

def set_db(new_db = None):
    
    if new_db != None:
        global db 
        global latest_scraper_version
        latest_scraper_version = "0.0.9"
        db = new_db

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
    print(query)

    cursor = db.articles.find(query).skip(offset).limit(limit)
    articles = []
    ids = []
    for dic in cursor:
        reports = process_reports(dic)
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


def process_reports(article):
    reports = []
    for report_dict in article['reports']:
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
    return reports


def get_reports(article_id):
    article = get_article_dict(article_id)
    reports = process_reports(article)
    return reports


def get_article_section(article_id, section_header):
    article = get_article_dict(article_id)
    return article['article_headers'][section_header]


def get_article_dict(article_id):
    article = db.articles.find_one({'id': article_id})
    if article is None:
        raise HTTPException(status_code=404, detail={"error_message": "No article found with that given id"})
    return article

logging.basicConfig(filename='result.log', level=logging.ERROR, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def start_logging(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as err:
            err_type, err_func, err_tb = sys.exc_info()

            logging.error(err_func)
            
            logging.error(''.join(traceback.format_tb(err_tb)))
            method = kwargs["request"].method
            url = kwargs["request"].url
            logging.error(method)
            logging.error(url)
            logging.error("The parameters that triggered this error")
            logging.error(kwargs)
            
            raise err

    return wrapper