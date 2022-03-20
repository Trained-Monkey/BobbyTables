import sys
import os

sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..', '..', 'API_SourceCode', 'API'))

from main import app
from fastapi.testclient import TestClient
from helpers import set_db
from test_helper import formulate_query_string, get_test_db

client = TestClient(app)

set_db(get_test_db())

"""
Tests article assessment route with invalid articleId
"""
def test_get_article_assessment_invalid_id():
    response = client.get("/article/100/assessment")
    assert response.status_code == 404
    assert response.json()["detail"] == {"error_message": "No article found with that given id"}

"""
Tests article assessment with id received from /article
"""
def test_get_article_assessment():
    query_string = formulate_query_string("Malawi", "2022-03-01T00:00:00", "2022-04-01T00:00:00", "outbreak")
    response = client.get("/article" + query_string)

    # Getting article id from base /article route
    # Needs an article in the database
    assert response.status_code == 200
    assert response.json()["max_articles"] > 0

    articleId = response.json()["articles"][0]["articleId"]
    response = client.get("/article/" + str(articleId) + "/assessment")

    assert response.status_code == 200

"""
Test article assessment with invalid version header
"""
def test_assessment_invalid_header():
    query_string = formulate_query_string("Malawi", "2022-03-01T00:00:00", "2022-04-01T00:00:00", "outbreak")
    response = client.get("/article" + query_string)

    articleId = response.json()["articles"][0]["articleId"]
    response = client.get("/article/" + str(articleId) + "/assessment", headers={"version": "qwer"})

    assert response.status_code == 422

"""
Test article assessment with version header
"""
def test_assessment_version_header():
    query_string = formulate_query_string("Malawi", "2022-03-01T00:00:00", "2022-04-01T00:00:00", "outbreak")
    response = client.get("/article" + query_string)

    articleId = response.json()["articles"][0]["articleId"]
    response = client.get("/article/" + str(articleId) + "/assessment", headers={"version": "v1.0"})

    assert response.status_code == 200
