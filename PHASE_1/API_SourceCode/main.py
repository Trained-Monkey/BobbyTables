from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi import Query, Header
from fastapi import status
from Type.Article import Article

tags_metadata = [
    {
        "name": "article",
        "description": "Operations on retrieving from articles",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

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
@app.get("/article", tags=["article"], response_model=Article)
async def article(
    end_date: str = Query(... ,example="2022-01-01T00:00:00", format="yyyy-MM-ddTHH:mm:ss"), 
    start_date: str = Query(...,example="2021-01-01T00:00:00", format="yyyy-MM-ddTHH:mm:ss"), 
    key_terms: str = Query(..., example="zika"),
    location: str = Query(..., example="vietnam"),
    limit: int = 20, 
    offset: int = 0,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')):
    return {"message" : "Article route not implemented"}

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
@app.get("/article/{articleId}/content", tags=["article"])
async def articleContent(
    articleId: int,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')):
    return {"message" : "Content route not implemented"}

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
@app.get("/article/{articleId}/response", tags=["article"])
async def articleResponse(
    articleId: int,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')):
    return {"message" : "Response route not implemented"}

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
@app.get("/article/{articleId}/assessment", tags=["article"])
async def articleAssessment(
    articleId: int,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')):
    return {"message" : "Assessment route not implemented"}

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
@app.get("/article/{articleId}/source", tags=["article"])
async def articleSource(
    articleId: int,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')):
    return {"message" : "Source route not implemented"}

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
@app.get("/article/{articleId}/advice", tags=["article"])
async def articleAdvice(
    articleId: int,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')):
    return {"message" : "Advice route not implemented"}

"""
Gets the reports contained in a given article

Headers:
 * version: string                - Version of the API 

Parameters:
 * articleId: integer, required   - Article to get content section from

Outputs:
 * report: [report]               - Reports found within the article

Example call: 
GET /article/1/report

Example resonse:
{
    "report": [<report object>]
}
"""
@app.get("/article/{articleId}/report", tags=["article"])
async def articleReport(
    articleId: int,
    version: str = Header("v1.0", regex='^v[0-9]+\.[0-9]+$')):
    return {"message" : "Report route not implemented"}


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
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
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title="Pandemic API",
        version="1.0",
        description="API to get information on pandemic articles extracted from the WHO website",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
