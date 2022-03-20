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
Tests article report route with invalid articleId
"""
def test_get_article_report_invalid_id():
    response = client.get("/article/100/reports")
    assert response.status_code == 404
    assert response.json()["detail"] == {"error_message": "No article found with that given id"}

"""
Tests article report with id received from /article
"""
def test_get_article_report():
    query_string = formulate_query_string("Malawi", "2022-03-01T00:00:00", "2022-04-01T00:00:00", "outbreak")
    response = client.get("/article" + query_string)


    # Getting article id from base /article route
    # Needs an article in the database
    assert response.status_code == 200
    assert response.json()["max_articles"] > 0
    reports = response.json()["articles"][0]["article"]["reports"]

    articleId = response.json()["articles"][0]["articleId"]
    response = client.get("/article/" + str(articleId) + "/reports")

    assert response.status_code == 200
    assert response.json()["reports"] == reports

"""
Test article report with invalid version header
"""
def test_report_invalid_header():
    query_string = formulate_query_string("Malawi", "2022-03-01T00:00:00", "2022-04-01T00:00:00", "outbreak")
    response = client.get("/article" + query_string)

    articleId = response.json()["articles"][0]["articleId"]
    response = client.get("/article/" + str(articleId) + "/reports", headers={"version": "qwer"})

    assert response.status_code == 422

"""
Test article report with version header
"""
def test_report_version_header():
    query_string = formulate_query_string("Malawi", "2022-03-01T00:00:00", "2022-04-01T00:00:00", "outbreak")
    response = client.get("/article" + query_string)

    articleId = response.json()["articles"][0]["articleId"]
    reports = response.json()["articles"][0]["article"]["reports"]
    
    response = client.get("/article/" + str(articleId) + "/reports", headers={"version": "v1.0"})

    assert response.status_code == 200
    assert response.json()["reports"] == reports
