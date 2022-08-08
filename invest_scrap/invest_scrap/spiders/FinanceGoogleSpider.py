import scrapy
from scrapy.selector import Selector
import logging
import json
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlencode
from urllib.parse import urlparse
from datetime import datetime
from bs4 import BeautifulSoup


class FinanceGoogleSpider(scrapy.Spider):
    name = 'FinanceGoogleSpider'

    
    logger = logging.getLogger(__name__)
 

    custom_settings = {'ROBOTSTXT_OBEY': False, 'LOG_LEVEL': 'INFO',

                       'CONCURRENT_REQUESTS_PER_DOMAIN': 10, 

                       'RETRY_TIMES': 5}
    
    def start_requests(self):
       
        
        start_urls = [
            self.finance_link
        ]
       

        for _url in start_urls: 
            yield scrapy.Request(_url, callback=self.parse, meta={'pos': 0})
        

    def parse(self, response):
        price = response.css('main div:nth-child(2) div:nth-child(1)').css('c-wiz div div div div div::text').get()
        yield {'price': price}
            