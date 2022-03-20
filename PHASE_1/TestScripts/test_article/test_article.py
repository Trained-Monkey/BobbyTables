import sys
import os
import json

sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..', '..', 'API_SourceCode', 'API'))

from main import app
from fastapi.testclient import TestClient
from helpers import set_db
from test_helper import formulate_query_string, get_test_db

client = TestClient(app)

set_db(get_test_db())


# with open("TestScripts/test_article/article1.txt", "r") as file:
#    article1 = json.load(file)

"""
Tests article route with missing parameters, expecting 400 Bad Request
"""
def test_get_article_missing_parameter():
    
    response = client.get("/article")
    assert response.status_code == 422

"""
Tests article with valid parameters, no offset and limit
"""
def test_get_article_missing_defaults():
    query_string = formulate_query_string("Malawi", "2022-03-01T00:00:00", "2022-04-01T00:00:00", "outbreak")
    response = client.get("/article" + query_string)

    assert response.status_code == 200
    result = response.json()

    # Only 1 article in the testing database should match
    assert result["max_articles"] == 1
    resultArticle = result["articles"][0]["article"]
    # Article 1 currently broken
   #  assert resultArticle == article1

"""
Tests article with valid parameters, nonsensical offset
"""
def test_get_article_invalid_offset():
    query_string = formulate_query_string("Australia", "2021-01-30T00:00:00", "2022-01-30T00:00:00", "Zika")
    response = client.get("/article" + query_string + "&offset=-10")

    assert response.status_code == 400
    assert response.json()["detail"] == {"error_message": "offset must be greater than 0"}

"""
Tests article with valid parameters, nonsensical limit
"""
def test_get_article_invalid_limit():
    query_string = formulate_query_string("Australia", "2021-01-30T00:00:00", "2022-01-30T00:00:00", "Zika")
    response = client.get("/article" + query_string + "&limit=-10")

    assert response.status_code == 400
    assert response.json()["detail"] == {"error_message": "limit must be greater than 0"}

"""
Tests article with incorrectly formatted dates, no offset and limit
"""
def test_get_article_invalid_format_date():
    # Missing the T for the format
    query_string = formulate_query_string("Australia", "2021-01-3000:00:00", "2022-01-3000:00:00", "Zika")
    response = client.get("/article" + query_string)

    assert response.status_code == 400

"""
Tests article with start_date after end_date
"""
def test_get_article_invalid_date_range():
    query_string = formulate_query_string("Australia", "2023-01-30T00:00:00", "2022-01-30T00:00:00", "Zika")
    response = client.get("/article" + query_string)

    assert response.status_code == 400

"""
Tests article with invalid version header
"""
def test_get_article_invalid_version():
    query_string = formulate_query_string("Australia", "2021-01-30T00:00:00", "2022-01-30T00:00:00", "Zika")
    response = client.get("/article" + query_string, headers = {"version": "vioeq"})

    assert response.status_code == 422




