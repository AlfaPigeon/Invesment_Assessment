from unittest import result
import scrapy
from scrapy.selector import Selector
import logging
import json
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlencode
from urllib.parse import urlparse
from datetime import datetime



class BISTGoogleSpider(scrapy.Spider):
    name = 'BISTGoogleSpider'

    
    logger = logging.getLogger(__name__)
 

    custom_settings = {'ROBOTSTXT_OBEY': False, 'LOG_LEVEL': 'INFO',

                       'CONCURRENT_REQUESTS_PER_DOMAIN': 10, 

                       'RETRY_TIMES': 5}
    
    def start_requests(self):
       
        
        start_urls = [
            f'http://www.google.com/search?q=inurl%3A+www.google.com/finance+{self.search_word}'
        ]
       

        for _url in start_urls: 
            yield scrapy.Request(_url, callback=self.parse, meta={'pos': 0})
        

    def parse(self, response):
        xlink = LinkExtractor()
        yield {'links':[i.url for i in xlink.extract_links(response) if 'https://www.google.com/finance/quote' in i.url and 'translate.google' not in i.url]}
            




            

      