import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..', 'API_SourceCode'))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

"""
Tests article route with invalid articleId
"""
def test_get_article_content():
    response = client.get("/article/-1/content")
    assert response.status_code == 400
    assert response.json() == {"error_message": "Bad request"}
