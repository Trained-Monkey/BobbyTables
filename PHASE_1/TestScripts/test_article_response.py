import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..', 'API_SourceCode'))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

"""
Tests article response route with invalid articleId
"""
def test_get_article_response():
    response = client.get("/article/-1/response")
    assert response.status_code == 400
    assert response.json() == {"error_message": "Bad request"}

"""
Tests article response with id received from /article
"""
def test_get_article_response():
    response = client.get("/article")

    # Getting article id from base /article route
    # Needs an article in the database
    assert response.status_code == 200
    assert response.json()["max_articles"] > 0

    articleId = response.json()["articles"][0]["articleId"]
    response = client.get("/article/" + str(articleId) + "/response")

    assert response.status_code == 200
