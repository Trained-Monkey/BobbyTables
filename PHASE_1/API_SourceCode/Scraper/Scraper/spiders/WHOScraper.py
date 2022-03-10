import scrapy

class Scraper(scrapy.Spider):
    name = 'WHOscraper'

    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'LOG_SHORT_NAMES': 'True',
        'LOG_FILE': 'loggy.txt',
        'LOG_STDOUT': 'True',
        'LOG_FILE_APPEND': 'False',
    }

    start_urls = ['https://www.who.int/emergencies/disease-outbreak-news']

    def parse(self, response):
        
        all_links = []
        all_titles = []

        print("========")
        print(f"Response code + url: {response}")
        print("========")
        obj_list = response.css('.sf-list-vertical')
        title_list = response.css('.full-title')
        for item in title_list:
            title = item.css('::text').get()
            all_titles.append(title)

        for item in obj_list:
            links = item.xpath('./a/@href').extract()
            for link in links:
                all_links.append(link)

        for i, item in enumerate(all_titles):
            print("=======")
            print(item)
            print(links[i])

        #print(f"Title: {response.css('.full-title')[0].css('::text').get()}")
        print("========")
        #print(f"Raw html: {response.text}")
        print("========")
        print(f"Next page object?: {response.css('a.next')[0]}")
        print("========")
        # response.follow will click this button essentially
        print(f"Next page button: {response.css('a.next')[0].css('::text').get()}")


        #for title in response.css('.oxy-post-title'):
        #    yield {'title': title.css('::text').get()}

        #for next_page in response.css('a.next'):
        #    yield response.follow(next_page, self.parse)
        