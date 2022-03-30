from fastapi import FastAPI, HTTPException, Request
from fastapi.openapi.utils import get_openapi
from fastapi import Query, Header
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# from fastapi import exception_handler
import json

import logging

import traceback
import sys

from Type.Article import Article, ArticleList, ArticleIDPair
from Type.Report import Report, ReportList
from Type.HTTP_Response import *
from fastapi.staticfiles import StaticFiles

import traceback


import helpers
from helpers import start_logging
from datetime import datetime

tags_metadata = [
    {
        "name": "Article",
        "description": "Operations on retrieving from articles",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

@app.exception_handler(RequestValidationError)
async def missing_parameters(request, exception):
    return JSONResponse({
        "error_message": "Bad request"
    }, status_code = 400)
    
"""
Routes set up according to stoplight documentation
link: https://bobbytables.stoplight.io/docs/pandemic-api/YXBpOjQzMjI3NTU4-pandemic-api
"""

"""
Gets a list of articles to according to parameters outlined in query string

Headers:
 * version: string                - Version of the API

Parameters:
 * end_date: string, required     - Inclusive end_date of publication range, format:yyyy-MM-ddTHH:mm:ss
 * start_date: string, required   - Inclusive start_date of publication range, format:yyyy-MM-ddTHH:mm:ss
 * key_terms: string, required    - Comma separated values of keyterms to be contained in articles
 * location: string, required     - Values of location to extract articles from
 * limit: integer                 - Maximum number of articles to return in list
 * offset: integer                - Number of articles to skip

Outputs:
 * max_articles: integer          - Maximum number of articles matching given parameters
 * articles: [{article, integer}] - List of article and its corresponding id

Example call: 
GET /article?start_date=yyyy-MM-ddTHH:mm:ss&end_date=yyyy-MM-ddTHH:mm:ss&key_terms=Zika&location=Australia

Example response:
{
    "articles": [{<article object>, 1}],
    "max_articles": 1
}
"""
responses = {
    400: {"model": HTTP_400},
    500: {"model": HTTP_500}
}
@app.get("/article", tags=["Article"], response_model=ArticleList, responses=responses, response_model_exclude_unset=True)
@start_logging
async def article(
    request: Request,
    end_date: str = Query(..., example="2022-01-01T00:00:00", format="yyyy-MM-ddTHH:mm:ss"),
    start_date: str = Query(..., example="2021-01-01T00:00:00", format="yyyy-MM-ddTHH:mm:ss"),
    key_terms: str = Query(..., example="outbreak"),
    location: str = Query(..., example="vietnam"),
    limit: int = 20,
    offset: int = 0,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')): # TODO: Handle API version
    """
    Gets a list of articles corresponding to the given input parameters
    """

    try:
        end_date_datetime = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
    except:
        raise HTTPException(status_code=400, detail={"error_message": "end_date must follow the format yyyy-MM-ddTHH:mm:ss"})
    
    try:
        start_date_datetime = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
    except:
        raise HTTPException(status_code=400, detail={"error_message": "start_date must follow the format yyyy-MM-ddTHH:mm:ss"})

    if (start_date_datetime > end_date_datetime):
        raise HTTPException(status_code=400, detail={"error_message": "start_date must be before end_date"})

    if (offset < 0):
        raise HTTPException(status_code=400, detail={"error_message": "offset must be greater than 0"})

    if (limit < 0):
        raise HTTPException(status_code=400, detail={"error_message": "limit must be greater than 0"})


    # Impose a maximum limit on the number of articles to return at once
    limit = min(limit, 50)

    terms_list = key_terms.split(',')
    articles, ids, max_articles = helpers.filter_articles(end_date_datetime, start_date_datetime, terms_list, location, limit, offset)
    zipped = zip(articles, ids)
    output = []
    for result in zipped:
        article_id_pair = ArticleIDPair(
            article=result[0],
            articleId=result[1]
        )
        output.append(article_id_pair)
    return {
        "articles": output,
        "max_articles": max_articles
    }
    

"""
Gets the content section for a given article

Headers:
 * version: string                - Version of the API

Parameters:
 * articleId: integer, required   - Article to get content section from

Outputs:
 * content: string                - Content section of the article

Example call: 
GET /article/1/content

Example response:
{
    "content": "Content section of article 1"
}
"""
responses = {
    404: {"model": HTTP_404},
    500: {"model": HTTP_500}
}
@app.get("/article/{articleId}/content", tags=["Article"], responses=responses)
@start_logging
async def article_content(
    request : Request,
    articleId: int,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')):
    """
    Gets the main content of the article with the given articleId
    """
    return {"content": helpers.get_article_section(articleId, "Content")}

"""
Gets the response section for a given article

Headers:
 * version: string                - Version of the API

Parameters:
 * articleId: integer, required   - Article to get response section from

Outputs:
 * response: string               - Response section of the article

Example call: 
GET /article/1/response

Example response:
{
    "response": "Response section of article 1"
}
"""
responses = {
    404: {"model": HTTP_404},
    500: {"model": HTTP_500}
}
@app.get("/article/{articleId}/response", tags=["Article"], responses=responses)
@start_logging
async def article_response(
    request : Request,
    articleId: int,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')):
    """
    Gets the response section of the article with the given articleId
    """
    return {"response": helpers.get_article_section(articleId, "Public health response")}

"""
Gets the assessment section for a given article

Headers:
 * version: string                - Version of the API

Parameters:
 * articleId: integer, required   - Article to get assessment section from

Outputs:
 * assessment: string             - Assessment section of the article

Example call: 
GET /article/1/assessment

Example response:
{
    "assessment": "Assessment section of article 1"
}
"""
responses = {
    404: {"model": HTTP_404},
    500: {"model": HTTP_500}
}
@app.get("/article/{articleId}/assessment", tags=["Article"], responses=responses)
@start_logging
async def article_assessment(
    request : Request,
    articleId: int,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')):
    """
    Gets the WHO risk assessment section of the article with the given articleId
    """
    return {"assessment": helpers.get_article_section(articleId, "WHO risk assessment")}

"""
Gets the source section for a given article

Headers:
 * version: string                - Version of the API

Parameters:
 * articleId: integer, required   - Article to get source section from

Outputs:
 * source: string                 - Source section of the article

Example call: 
GET /article/1/source

Example response:
{
    "source": "Source section of article 1"
}
"""
responses = {
    404: {"model": HTTP_404},
    500: {"model": HTTP_500}
}
@app.get("/article/{articleId}/source", tags=["Article"], responses=responses)
@start_logging
async def article_source(
    request : Request,
    articleId: int,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')):
    """
    Gets source url of the article with the given articleId
    """
    article_dict = helpers.get_article_dict(articleId)
    return {"source": article_dict['url']}

"""
Gets the advice section for a given article

Headers:
 * version: string                - Version of the API

Parameters:
 * articleId: integer, required   - Article to get advice section from

Outputs:
 * advice: string                 - Advice section of the article

Example call: 
GET /article/1/advice

Example resonse:
{
    "advice": "Advice section of article 1"
}
"""
responses = {
    404: {"model": HTTP_404},
    500: {"model": HTTP_500}
}
@app.get("/article/{articleId}/advice", tags=["Article"], responses=responses)
@start_logging
async def article_advice(
    request : Request,
    articleId: int,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')):
    """
    Gets the WHO health advice section of the article with the given articleId
    """
    return {"advice": helpers.get_article_section(articleId, "WHO advice")}

"""
Gets the reports contained in a given article

Headers:
 * version: string                - Version of the API 

Parameters:
 * articleId: integer, required   - Article to get content section from

Outputs:
 * reports: [report]               - Reports found within the article

Example call: 
GET /article/1/reports

Example response:
{
    "reports": [<report object>]
}
"""
responses = {
    404: {"model": HTTP_404},
    500: {"model": HTTP_500}
}
@app.get("/article/{articleId}/reports", tags=["Article"],  response_model=ReportList, responses=responses)
@start_logging
async def article_report(
    request : Request,
    articleId: int,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')):
    """
    Gets a list of reports detected in the article with the given articleId
    """
    reports = helpers.get_reports(articleId)
    return {"reports": reports}


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
# @start_logging
def perform_healthcheck():
    """
        Simple route for the GitHub Actions to healthcheck on.

        More info is available at:
        https://github.com/akhileshns/heroku-deploy#health-check

        It basically sends a GET request to the route & hopes to get a "200"
        response code. Failing to return a 200 response code just enables
        the GitHub Actions to rollback to the last version the project was
        found in a "working condition". It acts as a last line of defense in
        case something goes south.

        Additionally, it also returns a JSON response in the form of:

        {
          'healthcheck': 'Everything OK!'
        }
        """
    return {'healthcheck': 'Everything OK!'}

def custom_openapi():    
    with open("schema.json", "r+") as FILE:
        openapi_schema = json.load(FILE)

    openapi_schema["paths"]["/article/{articleId}/content"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["example"] = {"content" : "string"}
    openapi_schema["paths"]["/article/{articleId}/response"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["example"] = {"response" : "string"}
    openapi_schema["paths"]["/article/{articleId}/assessment"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["example"] = {"assessment" : "string"}
    openapi_schema["paths"]["/article/{articleId}/source"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["example"] = {"source" : "string"}
    openapi_schema["paths"]["/article/{articleId}/advice"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["example"] = {"advice" : "string"}

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
