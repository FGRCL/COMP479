import logging

import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from scrapy.exceptions import CloseSpider

from ir.p4.p4.indexer.indexer import Indexer


class Crawler(scrapy.Spider):
    name="concordia"
    start_urls = [
        'https://www.concordia.ca/'
    ]
    custom_settings = {
        # 'CONCURRENT_ITEMS': 8,
        # 'CONCURRENT_REQUESTS': 8,
        # 'SCHEDULER_PRIORITY_QUEUE': 'scrapy.pqueues.DownloaderAwarePriorityQueue',
        # 'REACTOR_THREADPOOL_MAXSIZE': 8

    }
    page_count = 0
    max_pages = -1
    indexer = Indexer()

    def __init__(self, category=None, *args, **kwargs):
        super().__init__(**kwargs)

        if 'max_pages' in kwargs:
            self.max_pages = int(kwargs['max_pages'])

    def parse(self, response, **kwargs):
        url = urlparse(response.url, allow_fragments=False)
        soup = BeautifulSoup(response.body)

        if self.max_pages < 0 or self.page_count <= self.max_pages:

            self.indexer.parse_web_page(soup, url)

            for element in soup.find_all('a'):
                link = element.get('href')
                if link is not None and link != '' and link[0] == '/':
                    parsed_link = urlparse(link)
                    new_url = url._replace(path=parsed_link.path)
                    yield scrapy.Request(new_url.geturl(), callback=self.parse)
        else:
            raise CloseSpider("Ran out of allocated pages")

        self.page_count += 1
        logging.info(f'Done parsing page {self.page_count}')

    def get_indexer(self) -> Indexer:
        return self.indexer
