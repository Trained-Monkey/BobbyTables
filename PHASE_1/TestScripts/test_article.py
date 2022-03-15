import sys
import os
import json


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

article1 = json.dumps({
   "url": "www.who.int/lalala_fake_article",
   "date_of_publication": "2018-12-12 xx:xx:xx",
   "headline": "Outbreaks in Southern Vietnam",
   "main_text": "Three people infected by what is thought to be H5N1 or H7N9  in Ho Chi Minh city. First infection occurred on 1 Dec 2018, and latest is report on 10 December. Two in hospital, one has recovered. Furthermore, two people with fever and rash infected by an unknown disease.",
   "reports": [
      {
         "event_date": "2018-12-01 xx:xx:xx to 2018-12-10 xx:xx:xx",
         "locations": [
            {
               "geonames-id": 1566083
            }
         ],
         "diseases": [
            "influenza a/h5n1",
            "influenza a/h7n9"
         ],
         "syndromes": [

         ]
      },
      {
         "event_date": "2018-12-01 xx:xx:xx to 2018-12-10 xx:xx:xx",
         "locations": [
            {
               "geonames-id":1566083
            }
         ],
         "diseases": [
            "unknown"
         ],
         "syndromes": [
            "Acute fever and rash"
         ]
      }
   ]
})

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
    query_string = formulate_query_string("Vietnam", "2018-12-11T00:00:00", "2018-12-13T00:00:00", "")
    response = client.get("/article" + query_string)

    assert response.status_code == 200
    result = response.json()

    # Only 1 article in the testing database should match
    assert len(result["max_articles"]) == 1
    resultArticle = result["articles"][0]["article"]
    assert resultArticle == article1

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
    query_string = formulate_query_string("Australia", "2023-01-30T00:00:00", "2022-01-30T00:00:00", "Zika")
    response = client.get("/article" + query_string)

    assert response.status_code == 400


"""
Tests article with invalid version header
"""
def test_get_article_invalid_version():
    query_string = formulate_query_string("Australia", "2021-01-30T00:00:00", "2022-01-30T00:00:00", "Zika")
    response = client.get("/article" + query_string, headers = {"version": "vioeq"})

    assert response.status_code == 400




