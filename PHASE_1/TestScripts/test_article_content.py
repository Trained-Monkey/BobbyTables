import sys
import os

sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..', 'API_SourceCode'))

from main import app
from fastapi.testclient import TestClient

"""
TODO: Override db function in main.py with testing db function
import pymongo

mongodb_username = quote_plus(os.getenv('MONGODB_USER'))
mongodb_password = quote_plus(os.getenv('MONBODB_PASSWORD'))

uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}" + \
      "@seng3011-bobby-tables.q2umd.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client.test

def get_db():
    return db

app.dependency_overrides[#GET_DB_FUNCTION] = get_db
"""

client = TestClient(app)

"""
Tests article content route with invalid articleId
"""
def test_get_article_content():
    response = client.get("/article/-1/content")
    assert response.status_code == 404
    assert response.json() == {"error_message": "No page found with given articleId"}

"""
Tests article content with id received from /article
"""
def test_get_article_content():
    response = client.get("/article")

    # Getting article id from base /article route
    # Needs an article in the database
    assert response.status_code == 200
    assert response.json()["max_articles"] > 0

    articleId = response.json()["articles"][0]["articleId"]
    response = client.get("/article/" + str(articleId) + "/content")

    assert response.status_code == 200

"""
Test article content with invalid version header
"""
def test_content_invalid_header():
    response = client.get("/article")
    articleId = response.json()["articles"][0]["articleId"]
    response = client.get("/article/" + str(articleId) + "/content", header={"version": "qwer"})

    assert response.status_code == 400
    assert response.json() == {"error_message": "Bad request"}

"""
Test article content with version header
"""
def test_content_version_header():
    response = client.get("/article")
    articleId = response.json()["articles"][0]["articleId"]
    response = client.get("/article/" + str(articleId) + "/content", header={"version": "v1.0"})

    assert response.status_code == 200
