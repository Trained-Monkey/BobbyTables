from urllib.parse import quote_plus
import pymongo

"""
Formulates a query string with parameters for /article route
"""
def formulate_query_string(location, start_date, end_date, keyterms):
    result = "?"
    
    result += "end_date="
    result += quote_plus(end_date)
    result += "&start_date="
    result += quote_plus(start_date)
    
    result += "&key_terms="
    result += quote_plus(keyterms)
    result += "&location="
    result += quote_plus(location)
    return result



"""
Gets the testing database to return
"""
def get_test_db():
    mongodb_username = 'bobbytest'
    mongodb_password = 'tablestest'

    uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}" + \
        "@seng3011-bobby-tables.q2umd.mongodb.net/test?retryWrites=true&w=majority"
    testClient = pymongo.MongoClient(uri)
    db = testClient.test

    return db