
import os
import json
import traceback
import re


import datefinder
import geograpy
import scrapy
from tqdm import tqdm
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

WINDOW_SIZE = 5
GENERAL_TERMS = ['outbreak', 'infection', 'fever', 'epidemic', 'infectious', 'illness', 'bacteria', 'emerging',
                 'unknown virus', 'mystery disease', 'mysterious disease']
SPECIFIC_TERMS = ['zika', 'mers', 'salmonella', 'legionnaire', 'measles', 'anthrax', 'botulism', 'plague',
                  'smallpox', 'tularemia', 'junin fever', 'machupo fever', 'guanarito fever', 'chapare fever',
                  'lassa fever', 'lujo fever', 'hantavirus', 'rift valley fever',
                  'crimean congo hemorrhagic fever', 'dengue', 'ebola',
                  'marburg']  # TODO: Add 'other related pox viruses
WINDOW_THRESHOLD = 3


class WHOScraper(CrawlSpider):
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
        # Rule(LinkExtractor(allow=r'\d+'), follow=True), # TODO: Re-enable this once we have it works on one site

    )

    def parse_article(self, response):
        if response.url != 'https://www.who.int/emergencies/disease-outbreak-news/item/wild-poliovirus-type-1-(WPV1)-malawi':
            return
        article = response.xpath('//article')
        article_text = ""
        if article is not None:
            for p in article.xpath('.//p/text()'):
                article_text += p.get()
        article_url = response.url
        article_date = response.xpath("//span[contains(@class, 'timestamp')]/text()").get()
        article_headline = response.xpath("//h1/text()").get().strip('\n')
        # article_reports = self.find_reports(article_text)  # TODO: Fix reports to actually generate reports
        test = self.find_reports("Three people infected by what is thought to be H5N1 or H7N9  in Ho Chi Minh city. First infection occurred on 1 Dec 2018, and latest is report on 10 December. Two in hospital, one has recovered. Furthermore, two people with fever and rash infected by an unknown disease.")

    # WIP
    # This is a basic implementation, though words we are looking for need to be improved so we can successfully detect
    # words that are in a report, and so we can generate a report

    def find_reports(self, text):
        # print(geograpy.get_place_context("H7N9  in Ho Chi Minh"))

        # We only need to search the article up until 'Further information'
        split_text = text.split('\xa0\xa0\xa0')
        text = split_text[0]

        # Test
        with open(os.path.join(os.path.dirname(__file__), '../../syndrome_list.json')) as f:
            syndrome_list = json.load(f)
        with open(os.path.join(os.path.dirname(__file__), '../../diseases.json')) as f:
            disease_list = json.load(f)

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
            window_score = 0
            contains_date = False
            contains_location = False
            contains_disease = False
            matched_disease_list = []
            contains_syndrome = False
            matched_syndrome_list = []

            dates = datefinder.find_dates(window_string)
            if len(list(dates)) > 0:
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
                if syndrome.lower() in window_string.lower():
                    contains_syndrome = True
                    matched_syndrome_list.append(syndrome)

            # print(f"{start_window_index}: {window_string}")
            places = geograpy.get_place_context(text=window_string)
            if len(places.countries) > 0 or len(places.regions) > 0 or len(places.cities) > 0 or len(places.other) > 0:
                contains_location = True
            else:
                if 'city' in window_string or 'City' in window_string:
                    r = re.compile(r'(([A-Z][a-z-]+)+ )+[Cc]ity')
                    result = r.match(window_string)
                    if result is not None:
                        print(result.group(0))
                        print(geograpy.locateCity(result.group(0)))
                        places.cities.append(result.group(0))

            # my regex: ^(\d{2}) (\w+) (\d{4})$
            # report regex: ^(\  d{4})-(\d\d|xx)-(\d\d|xx) (\d\d|xx):(\d\d|xx):(\d\d|xx)$

            report_dict = {
                'index': int(start_window_index + (WINDOW_SIZE / 2)),
                'dates': list(dates),
                'locations': places.cities + places.regions + places.countries,
                'diseases': list(matched_disease_list),
                'syndromes': list(matched_syndrome_list),
                'debug': {
                    'location_others': places.other
                }
            }

            print(f"{start_window_index}\t\t{places.cities + places.regions + places.countries}")
            #print(f"{window_string}")
            #print(f"Date: {contains_date}, Location: {contains_location}, Syndrome: {contains_syndrome}, Disease: {contains_disease}")
            if contains_date and contains_location and (contains_syndrome or contains_disease):
                matches.append(report_dict)

            start_window_index += 1
            end_window_index += 1
            progress_bar.update(1)
        progress_bar.close()
        for match in matches:
            print(match)
        with open('output.json', 'w') as f:
            json.dump(matches, f)
        return []  # TODO: Return matches once we actually generate them
