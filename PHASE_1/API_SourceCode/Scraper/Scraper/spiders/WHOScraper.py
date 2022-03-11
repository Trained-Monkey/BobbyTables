import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

WINDOW_SIZE = 10
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

    allowed_domains = ['who.int']

    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'LOG_SHORT_NAMES': 'True',
        'LOG_FILE': 'loggy.txt',
        'LOG_STDOUT': 'True',
        'LOG_FILE_APPEND': 'False',
    }

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
        article_reports = self.find_reports(article_text)  # TODO: Fix reports to actually generate reports

    # WIP
    # This is a basic implementation, though words we are looking for need to be improved so we can successfully detect
    # words that are in a report, and so we can generate a report
    def find_reports(self, text):
        text_words = text.lower().split(' ')
        start_window_index = 0
        end_window_index = WINDOW_SIZE
        combined_words = GENERAL_TERMS + SPECIFIC_TERMS
        matches = []
        # Start moving the window through the paragraph
        while end_window_index < len(text_words):
            window = text_words[start_window_index:end_window_index]
            window_score = 0
            # Iterate through all words we think it could be
            for word in combined_words:
                # If the symptom composes of multiple words, we need to make sure the next couple of words match as well
                if word.count(' ') > 0:
                    split_words = word.split(' ')
                    full_match = True
                    for split_word in split_words:
                        if split_word in window:  # This could be improved to make sure the next word is the match
                            window_score += 1
                        else:
                            full_match = False
                    # Rate a match higher if every word in a multi-word term is matched
                    if full_match:
                        window_score += 10  # TODO: Find better default
                    pass
                else:
                    # We only need to make sure a single word is in
                    if word in window:
                        window_score += 1
                if window_score >= WINDOW_THRESHOLD:
                    matches.append(window) # Temp fix to see what our matches look like
            start_window_index += 1
            end_window_index += 1
        print(matches)
        return [] # TODO: Return matches once we actually generate them
