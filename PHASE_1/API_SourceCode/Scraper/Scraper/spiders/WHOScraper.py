from asyncio import start_server
import os
import json
import sys
import traceback
import re
import time
import datetime
from urllib.parse import quote_plus

from dotenv import load_dotenv
import pymongo
import datefinder
import geograpy
import scrapy
import nltk
from tqdm import tqdm
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from google.cloud import language_v1

SCRAPER_VERSION = '0.0.7'

WINDOW_SIZE = 26
GENERAL_TERMS = ['outbreak', 'infection', 'fever', 'epidemic', 'infectious', 'illness', 'bacteria', 'emerging',
                 'unknown virus', 'mystery disease', 'mysterious disease']
SPECIFIC_TERMS = ['zika', 'mers', 'salmonella', 'legionnaire', 'measles', 'anthrax', 'botulism', 'plague',
                  'smallpox', 'tularemia', 'junin fever', 'machupo fever', 'guanarito fever', 'chapare fever',
                  'lassa fever', 'lujo fever', 'hantavirus', 'rift valley fever',
                  'crimean congo hemorrhagic fever', 'dengue', 'ebola',
                  'marburg']  # TODO: Add 'other related pox viruses
WINDOW_THRESHOLD = 3

load_dotenv()
mongodb_username = quote_plus(os.getenv('MONGODB_USER'))
mongodb_password = quote_plus(os.getenv('MONBODB_PASSWORD'))
uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}" + \
      "@seng3011-bobby-tables.q2umd.mongodb.net/api?retryWrites=true&w=majority"

client = pymongo.MongoClient(uri)
db = client.api
cache_db = client.cache


def convert_entity_list_to_json(response: language_v1.types.AnalyzeEntitiesResponse):
    ls = []
    for entity in response.entities:
        dic = {
            "name": entity.name,
            "type_": entity.type_,
            "salience": entity.salience,
        }
        if entity.metadata is not None:
            metadata = []
            for metadit in entity.metadata:
                metadata.append({metadit: entity.metadata[metadit]})
            dic.update({'metadata': metadata})
        ls.append(dic)
    return ls


def set_up_google_cloud_service_account():
    global gc_client
    obj = {
        "type": "service_account",
        "project_id": "seng3011-scraper",
        "private_key_id": f"{str(os.getenv('GC_SERVICE_ACC_PRIVATE_KEY_ID'))}",
        "private_key": f"{format(os.getenv('GC_SERVICE_ACC_PRIVATE_KEY'))}",
        "client_email": f"{str(os.getenv('GC_SERVICE_ACC_CLIENT_EMAIL'))}",
        "client_id": f"{str(os.getenv('GC_SERVICE_ACC_CLIENT_ID'))}",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/nat-lang-serv-acct%40seng3011-scraper.iam.gserviceaccount.com"
    }
    with open(os.path.join(os.path.dirname(__file__), '..', '..', 'service_account.json'), 'w') as f:
        obj_str = json.dumps(obj)
        f.write(obj_str.replace('\\\\', '\\'))
    time.sleep(1)
    gc_client = language_v1.LanguageServiceClient.from_service_account_json(
        os.path.join(os.path.dirname(__file__), '..', '..', 'service_account.json'))


def set_up_nltk():
    nltk.downloader.download('maxent_ne_chunker')
    nltk.downloader.download('words')
    nltk.downloader.download('treebank')
    nltk.downloader.download('maxent_treebank_pos_tagger')
    nltk.downloader.download('punkt')
    # since 2020-09
    nltk.downloader.download('averaged_perceptron_tagger')


def get_new_article_id():
    if db.articles.count_documents({'id': {'$exists': True}}, limit=1) == 0:
        return 1
    return db.articles.find_one({}, sort=[("id", pymongo.DESCENDING)])['id'] + 1


class WHOScraper(CrawlSpider):

    def __init__(self):
        # set_up_nltk()
        set_up_google_cloud_service_account()
        super().__init__()

    name = 'WHOScraper'

    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'LOG_SHORT_NAMES': 'True',
        'LOG_FILE': 'loggy.txt',
        'LOG_STDOUT': 'True',
        'LOG_FILE_APPEND': 'False',
    }

    allowed_domains = ['who.int']

    start_urls = ['https://www.who.int/emergencies/disease-outbreak-news']

    rules = (
        Rule(LinkExtractor(allow=r'/item/'), callback='parse_article'),
        Rule(LinkExtractor(allow=r'\d+'), follow=True),  # TODO: Re-enable this once we have it works on one site

    )

    def parse_article(self, response):
        updating = False
        id_to_use = get_new_article_id()
        if db.articles.count_documents({'url': response.url}, limit=1) != 0:
            # Check if the document we do already have has been parsed with the same SCRAPER_VERSION
            exists = db.articles.count_documents({'url': response.url, 'scraper_version': SCRAPER_VERSION},
                                                 limit=1) == 1
            if exists:
                return
            else:
                existing_article = db.articles.find_one({'url': response.url})
                if 'id' in existing_article:
                    id_to_use = existing_article['id']
                updating = True
        article = response.xpath('//article')
        article_text = ""
        if article is not None:
            for p in article.xpath(".//p/text() | .//li/text()"):
                article_text += p.get()
        article_url = response.url
        article_date = response.xpath("//span[contains(@class, 'timestamp')]/text()").get()
        date_object = datetime.datetime.strptime(article_date, "%d %B %Y")
        article_headline = response.xpath("//h1/text()").get().strip('\n')
        article_reports = self.find_reports(article_text)
        article_locations = []
        for report in article_reports:
            article_locations += report['locations']
        article_terms = self.find_search_terms(article_text)
        output = {
            'url': article_url,
            'date_of_publication': date_object,
            'headline': article_headline,
            'main_text': article_text,
            'reports': article_reports,
            'scraper_version': SCRAPER_VERSION,
            'search_terms': article_terms,
            'locations': article_locations,
            'id': id_to_use
        }
        if updating:
            db.articles.update_one({'url': article_url}, output)
        else:
            db.articles.insert_one(output)

        # test = self.find_reports("Three people infected by what is thought to be H5N1 or H7N9  in Ho Chi Minh city.
        # First infection occurred on 1 Dec 2018, and latest is report on 10 December. Two in hospital,
        # one has recovered. Furthermore, two people with fever and rash infected by an unknown disease.")

    def find_search_terms(self, text):
        matches = []
        terms = GENERAL_TERMS + SPECIFIC_TERMS
        for term in terms:
            if term.lower() in text.lower():
                matches.append(term)
        return matches


    # WIP
    # This is a basic implementation, though words we are looking for need to be improved so we can successfully detect
    # words that are in a report, and so we can generate a report

    def find_reports(self, text):
        # We only need to search the article up until 'Further information'
        split_text = text.split('\xa0\xa0\xa0')
        text = split_text[0]

        # Test
        with open(os.path.join(os.path.dirname(__file__), '../../syndrome_list.json')) as f:
            syndrome_list = json.load(f)
        with open(os.path.join(os.path.dirname(__file__), '../../diseases.json')) as f:
            disease_list = json.load(f)

        #### LOCATION PARSING
        # Check if the text has already been parsed
        if cache_db.entities.count_documents({'text': text}, limit=1) == 0:
            # Parse text
            document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
            entities = gc_client.analyze_entities(document=document)
            converted_entities = convert_entity_list_to_json(entities)

            # Upload to cache
            cache_db.entities.insert_one({'text': text, 'entities': converted_entities})
            entities = converted_entities
        else:
            # Load data from cache
            cached_obj = cache_db.entities.find_one({'text': text})
            entities = cached_obj['entities']

        # Find things we need to pay attention to:
        entity_locations = []
        for entity in entities:
            if entity['type_'] == language_v1.types.Entity.Type.LOCATION:
                entity_locations.append(entity['name'])

        text_words = text.split(' ')
        start_window_index = 0
        end_window_index = start_window_index + WINDOW_SIZE
        combined_words = GENERAL_TERMS + SPECIFIC_TERMS
        matches = []
        # Start moving the window through the paragraph
        progress_bar = tqdm(total=(len(text_words) - WINDOW_SIZE))
        while end_window_index <= len(text_words):
            # print(f'{end_window_index} < {len(text_words)}')
            window = text_words[start_window_index:end_window_index]
            window_string = ' '.join(window)
            contains_date = False
            contains_location = False
            contains_disease = False
            matched_disease_list = []
            contains_syndrome = False
            matched_syndrome_list = []

            dates = datefinder.find_dates(window_string)
            dates_list = list(dates)
            if len(dates_list) > 0:
                contains_date = True

            for disease_obj in disease_list:
                # Diseases like "influenza a/h5n1" are often refered to as "H5N1"
                # Search for the name after the /
                disease = disease_obj['name']
                if '/' in disease:
                    sub_disease_words = disease.split('/')
                    for sub_disease in sub_disease_words:
                        if sub_disease in window_string.lower():
                            contains_disease = True
                            matched_disease_list.append(disease)
                # Search for the whole string
                if disease in window_string.lower():
                    contains_disease = True
                    matched_disease_list.append(disease)

            for syndrome_obj in syndrome_list:
                syndrome = syndrome_obj['name']
                if syndrome.lower().startswith('acute'):
                    # There may be symptoms that are not acute, try searching for those
                    split_syndrome = syndrome.lower().split('acute ')
                    merged_syndrome = ' '.join(split_syndrome)
                    while merged_syndrome.startswith(' '):
                        merged_syndrome = merged_syndrome[1:]
                    if merged_syndrome in window_string.lower():
                        contains_syndrome = True
                        matched_syndrome_list.append(syndrome)
                if syndrome.lower() in window_string.lower():
                    contains_syndrome = True
                    matched_syndrome_list.append(syndrome)

            # TODO: Get location data window from the pre-parsed entity data, and extract locations for this window
            locations = []
            for entity_location in entity_locations:
                if entity_location in window_string:
                    contains_location = True
                    locations.append(entity_location)

            valid_locations = []
            counter = 0
            with open(os.path.join(os.path.dirname(__file__), '../../location_data.json'), encoding='utf-8') as f:
                for line in f:
                    line = line.lstrip()
                    if line.startswith("\"name\": "):
                        line = re.sub(r'"name": ', '', line)
                    elif line.startswith("\"states\": ") or line.startswith("\"cities\": "):
                        continue
                    elif line.startswith("{") or line.startswith("}") or line.startswith("]"):
                        continue
                    else:
                        line = line[1:-2]

                    for location in locations:
                        if line.startswith(location):
                            valid_locations.append(line)
            locations = valid_locations

            report_dict = {
                'index': int(start_window_index + (WINDOW_SIZE / 2)),
                'dates': dates_list,
                'locations': locations,
                'diseases': list(matched_disease_list),
                'syndromes': list(matched_syndrome_list),
                'debug': {
                }
            }

            if contains_date and contains_location and (contains_syndrome or contains_disease):
                matches.append(report_dict)

            start_window_index += 1
            end_window_index += 1
            progress_bar.update(1)
        progress_bar.close()
        consolidated = consolidate_matches(matches)

        # Format to expected format
        output = []
        for match in consolidated:
            if len(match['dates']) == 1:
                event_date = match['dates'][0].strftime("%Y-%m-%d %H:%M:%S")
            else:
                event_date = f"{match['dates'][0].strftime('%Y-%m-%d %H:%M:%S')} to {match['dates'][1].strftime('%Y-%m-%d %H:%M:%S')}"
            formatted = {
                'event-date': event_date,
                'locations': match['locations'],
                'diseases': match['diseases'],
                'syndromes': match['syndromes']
            }
            output.append(formatted)
        with open('output.json', 'w') as f:
            json.dump(output, f)
        return output


def consolidate_matches(matches):
    groups = {}
    group_data = {}
    prev_index = None
    current_index = None
    latest_group_number = 1
    # Group all reports
    count = 0
    for match in matches:
        count += 1
        current_index = match['index']
        if prev_index is None or current_index - prev_index <= 1:
            pass
        else:
            group_data[latest_group_number]['max_index'] = prev_index
            latest_group_number += 1
        if f"group {latest_group_number}" not in groups:
            groups[f'group {latest_group_number}'] = []
            group_data[latest_group_number] = {}
            group_data[latest_group_number]['min_index'] = current_index
        groups[f'group {latest_group_number}'].append(match)
        if count == len(matches):
            group_data[latest_group_number]['max_index'] = current_index
        prev_index = current_index

    # Pick best reports from each group
    group_numbers = group_data.keys()
    wanted_indexes = []
    for group_number in group_numbers:
        if group_number == min(group_numbers):
            wanted_indexes.append(group_data[group_number]['min_index'])
        elif group_number == max(group_numbers):
            wanted_indexes.append(group_data[group_number]['max_index'])
        else:
            max_below = group_data[group_number - 1]['max_index']
            min_above = group_data[group_number + 1]['min_index']
            max_distance = 0
            max_distance_index = None
            for match in groups[f"group {group_number}"]:
                distance_below = match['index'] - max_below
                distance_above = min_above - match['index']
                average_distance = (distance_above + distance_below) / 2
                if average_distance > max_distance:
                    max_distance = average_distance
                    max_distance_index = match['index']
            wanted_indexes.append(max_distance_index)
    output = []
    for match in matches:
        if match['index'] in wanted_indexes:
            output.append(match)
    return output
