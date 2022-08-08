from unittest import result
import scrapy
from scrapy.selector import Selector
import logging
class CrunchbaseSpider(scrapy.Spider):
    name = 'CrunchbaseSpider'

    #cdk-describedby-message-{key}
    info_map ={
        1:'Location',
        2:'Employee_Count',
        3:'Funding_Type',
        4:'IPO_Status',
        5:'Website',
        6:'CB_Rank',
        7:'Acquisition_Count',
        8:'Total_Funding',
        9:'Total_Crunchbase_Contacts',
        10:'Total_Employee_Profiles_Crunchbase',
        11:'Investor_Count',
        12:'Similar_Organization_Count',
        13:'Prermium_Feature',
        14:'Descriptive_keyword',
        15:'Headquater_Location',
        16:'Foundation_Date',
        17:'Founders',
        18:'Status',
        19:'Last_Funding_Type',
        20:'Alternate_Name',
        21:'Legal_Name',
        22:'Tags',
        23:'Profit',
        24:'Email',
        25:'Phone'

    }
    
    logger = logging.getLogger(__name__)
    custom_settings = {'ROBOTSTXT_OBEY': False, 'LOG_LEVEL': 'INFO',

                       'CONCURRENT_REQUESTS_PER_DOMAIN': 10, 

                       'RETRY_TIMES': 5,
                       'DEFAULT_REQUEST_HEADERS':{
                           ':authority' :'www.crunchbase.com',
                            'Referer': 'http://crunchbase.com/companies',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'document',
                            'sec-fetch-mode': 'navigate',
                            'sec-fetch-site': 'same-origin',
                            'sec-fetch-user': '?1',
                            'upgrade-insecure-requests': '1',
                            'cookie': '__cflb=02DiuJLCopmWEhtqNz4kLo55nWiP3znDiSM6TLaELxTWc; xsrf_token=Wvi6zFVcQLMVUO898xIFjGg1GFl4UZjXdAAkW101vGo; cid=CigUY2LCsJAaowAslQvgAg==; pxcts=5e62b158-fb7a-11ec-ab2d-736964556544; _pxvid=5e62a399-fb7a-11ec-ab2d-736964556544; _pxhd=Gqv/rPHcQYrlZtZ7KzNFhk4xtqU2O8RHgyyb1yucS4HxYfv4zK9YBLL5nJIDlsMXy6e/z37Wd7f4BNL5iEZ54w; _px3=2e6cc9c299e88991bc0269488cd6b3f4c0fbb6fc7aa2a164eed77e399065d7ae:LuYhdMkydLmHfrfqJU3CgvCA6G4K+KK9HnPG3LNe+3bgGT2E0MdfqXnQQ+Bt2m3odLec8WZBg/ZMy3V5Dh0R4w==:1000:mL3t4vvva3qoTzS6fXRNja6pYKqnFor0lTj7aIhEFNRhrI/sJ4cNNsRuH4tgcj2nAL3tcc4O0KnFOx1N4jG0zzuoBPvbNICbeNCCEPl9PGiYBHLGm5XlswKiFuA4BymPLL6kAoLnwCYGhKNkKOpAPUF0fVJIwEoVoFTXww8JXxV0nblvi6mk6wTEsjivc72MpsxsA56+qKLb5P+zAtEH0A=='}
                        }
        
        
    def start_requests(self):
       
        start_urls = [
            self.firm_url
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    #Selector
    def get_info(self, list_element):
        field = Selector(text=list_element)
        
        descriptor=field.css('theme-icon::attr(aria-describedby)').get()
        if(descriptor is None or descriptor is "hidden"):
            descriptor=field.css('icon::attr(aria-describedby)').get()
        if(descriptor is None or descriptor is "hidden"):
            return None
        
        self.logger.info("desc===============id: "+descriptor)

        #get value
        result = ""
        _key =self.info_map[descriptor]
        if(_key == "IPO Status"):
            result = field.css('span::text').get() 
        elif(_key == "Descriptive keyword for an Organization (e.g. SaaS, Android, Cloud Computing, Medical Device)"):
            result="|".join(field.css('a').css('div::text').getall())
        elif(_key == "Price of the acquisition" or _key == "Date the Acquisition was announced" or _key =="Operating Status of Organization e.g. Active, Closed" or _key == "Date the Organization was founded" or _key == "Whether an Organization is for profit or non-profit" or _key == "Alternate or previous names for the organization"):
            result=field.css('field-formatter').css('span::text').get()
        elif(_key=="General contact email for the organization" or _key=="Organization's general phone number" or _key == "The legal name of the organization"):
            result=field.css('field-formatter').css('blob-formatter').css('span::text').get()
        elif(_key=="Tags are labels assigned to organizations, which identify their belonging to a group with that shared label"):
            result=" ".join(field.css('field-formatter').css('enum-multi-formatter').css('span::text').getall())
        elif(_key=="Name of the organization that made the acquisition" or _key =="Auto-generated name of transaction (e.g. WhatsApp acquired by Facebook)"):
            result=field.css('field-formatter').css('identifier-formatter').css('a').css('div').css('div::text').get()
        else:
            result=" ".join(field.css('a::text').getall())
        
            
            
        try:
            return [self.info_map[descriptor] ,result]
        except:
            self.logger.warning("===============id: "+descriptor)
            return None
        
        
    def get_highlight_info(self,list_element):
        field = Selector(text=list_element)
        
        descriptor=field.css('theme-icon::attr(aria-describedby)').get()
        if(descriptor is None or descriptor is "hidden"):
            descriptor=field.css('icon::attr(aria-describedby)').get()
        if(descriptor is None or descriptor is "hidden"):
            return None
        
        self.logger.info("desc===============id: "+descriptor)

        #get value
        result = ""
        
        _key =self.info_map[descriptor]
        result=field.css('field-formatter').css('span::text').get()
            
            
        try:
            return [self.info_map[descriptor] ,result]
        except:
            self.logger.warning("===============id: "+descriptor)
            return None      
        
        
    def parse(self, response):

        self.info_map = {}
        _keys =response.css('.cdk-describedby-message-container').css('div::attr(id)').getall()
        _vals = response.css('.cdk-describedby-message-container').css('div::text').getall()
        for i in range(len(_keys)):
            self.info_map[_keys[i]]=_vals[i]
        
        self.logger.info("############# info_map: "+str(self.info_map))
        company_name = response.css(".profile-name::text").get()
        
        profile_sec = response.css('profile-section')
        
        #company_description = profile_sec1.css(".description::text").get()
        
        
        

        _result= {}
        _result["Company_Name"]=company_name
        
        sec_list=profile_sec.css('ul').css('li').getall()
        for li in sec_list:
            _info = self.get_info(li)
            if(_info is not None):
                _result[_info[0]]=_info[1]
        
        highlight_list=response.css('profile-section').css('anchored-values').css('div').css('a').getall()
        for a in highlight_list:
            _info = self.get_highlight_info(a)
            if(_info is not None):
                _result[_info[0]]=_info[1]
                
                
        yield _result
                
      


            

      