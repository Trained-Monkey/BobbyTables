import sys
import os


sys.path.insert(1, os.path.join(sys.path[0], '..', 'API_SourceCode'))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

"""
Formulates a query string with parameters for /article route
"""
def formulate_query_string(location, start_date, end_date, keyterms):
    result = "?"
    result += "location="
    result += location
    result += "&start_date="
    result += start_date
    result += "&end_date="
    result += end_date
    result += "&keyterms="
    result += keyterms
    return result

"""
Date format: yyyy-MM-ddTHH:mm:ss
"""

"""
Tests article route with missing parameters, expecting 400 Bad Request
"""
def test_get_article_missing_parameter():
    response = client.get("/article")
    assert response.status_code == 400
    assert response.json() == {"error_message": "Bad request"}

"""
Tests article with valid parameters, no offset and limit
"""
def test_get_article_missing_defaults():
    query_string = formulate_query_string("Australia", "2021-01-30T00:00:00", "2022-01-30T00:00:00", "Zika")
    response = client.get("/article" + query_string)

    assert response.status_code == 200
    result = response.json()

    # Default limit should be set to 20
    assert len(result["articles"]) == 20

"""
Tests article with valid parameters, nonsensical offset
"""
def test_get_article_invalid_offset():
    query_string = formulate_query_string("Australia", "2021-01-30T00:00:00", "2022-01-30T00:00:00", "Zika")
    response = client.get("/article" + query_string + "&offset=-10")

    assert response.status_code == 400

"""
Tests article with valid parameters, nonsensical limit
"""
def test_get_article_invalid_limit():
    query_string = formulate_query_string("Australia", "2021-01-30T00:00:00", "2022-01-30T00:00:00", "Zika")
    response = client.get("/article" + query_string + "&limit=-10")

    assert response.status_code == 400

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
    query_string = formulate_query_string("Australia", "2023-01-3000:00:00", "2022-01-3000:00:00", "Zika")
    response = client.get("/article" + query_string)

    assert response.status_code == 400


"""
Tests article with invalid version header
"""
def test_get_article_invalid_version():
    query_string = formulate_query_string("Australia", "2021-01-3000:00:00", "2022-01-3000:00:00", "Zika")
    response = client.get("/article" + query_string, headers = {"version": "vioeq"})

    assert response.status_code == 400




