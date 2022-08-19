import json
from unittest import result
from flask import Flask
from flask import request
from flask_cors import CORS
import  psycopg2 
import threading
import sys
import subprocess
import scrapyrt
import requests
import time
import finnhub
import datetime

finnhub_client = finnhub.Client(api_key="cb6407qad3i70tu5u2tg")
app = Flask(__name__)
CORS(app)
#scrapy server
def scrapy_crunchbase_server_endpoint(firm_url):
    return f'http://localhost:3000/crawl.json?start_requests=true&spider_name=CrunchbaseSpider&crawl_args=%7B%22firm_url%22%3A%22{firm_url}%22%7D'
def scrapy_crunchbase_google_server_endpoint(search_word):
    return f'http://localhost:3000/crawl.json?start_requests=true&spider_name=CrunchbaseGoogleSpider&crawl_args=%7B%22search_word%22%3A%22{search_word}%22%7D'
def scrapy_bist_google_scrap_endpoint(search_word):
    return f'http://localhost:3000/crawl.json?start_requests=true&spider_name=BISTGoogleSpider&crawl_args=%7B%22search_word%22%3A%22{search_word}%22%7D'
def scrapy_bist_google_finance_endpoint(finance_link):
    return f'http://localhost:3000/crawl.json?start_requests=true&spider_name=FinanceGoogleSpider&crawl_args=%7B%22finance_link%22%3A%22{finance_link}%22%7D'
def start_scrapy_server():
    print("starting scrapy server..")
    time.sleep(0.5)
    command = ['invest\Scripts\python.exe', 'invest_scrap/start_scrapy_server.py']
    subprocess.call(command)


scrapy_server = threading.Thread(target=start_scrapy_server)
scrapy_server.start()
#=====================================================================================================
#finhub functions
def finnhub_symbol_lookup(search):
    global finnhub_client
    return finnhub_client.symbol_lookup(search)

def finnhub_company_profile(symbol):
    global finnhub_client
    return finnhub_client.company_profile2(symbol=symbol)

def finnhub_general_news():
    global finnhub_client
    return finnhub_client.general_news('general', min_id=0)

def finnhub_company_new(symbol, _from, to):
    global finnhub_client
    finnhub_client.company_news(symbol, _from=_from, to=to)

def finnhub_company_peers(symbol):
    global finnhub_client
    finnhub_client.company_peers(symbol)
    
def finnhub_company_basic_financials(symbol):
    global finnhub_client
    finnhub_client.company_basic_financials(symbol,'all')    

def finnhub_finnhub_stock_insider_transactions(symbol):
    global finnhub_client
    return finnhub_client.stock_insider_transactions(symbol=symbol)

def finnhub_stock_insider_sentiment(symbol,_from,_to):
    global finnhub_client
    return finnhub_client.stock_insider_sentiment(symbol,_from,_to)

def finnhub_financials_reported(symbol):
    global finnhub_client
    return finnhub_client.financials_reported(symbol=symbol, freq='annual')

def finnhub_financials_reported(symbol):
    global finnhub_client
    return finnhub_client.financials_reported(symbol=symbol, freq='annual')

def finnhub_ipo_calendar(_from,_to):
    global finnhub_client
    return finnhub_client.ipo_calendar(_from,_to)

def finnhub_recommendation_trends(symbols):
    global finnhub_client
    return finnhub_client.recommendation_trends(symbol=symbols)

def finnhub_stock_candles(symbol):
    global finnhub_client
    ms = datetime.datetime.now()
    return finnhub_client.stock_candles(symbol, 'D', int(time.mktime(ms.timetuple())-864000),int( time.mktime(ms.timetuple())))
#=====================================================================================================

#Flask functions
@app.route('/')
def index():
    response = requests.get(scrapy_crunchbase_google_server_endpoint('turk telekom'))
    return json.dumps({
        'endpoints':[
            {'path':'/symbol_lookup','desc':'symbol lookup using finnhub service','usage':'?search= <search keyword>'},
            {'path':'/crunchbase_google_search','desc':'by using google scraping finds crunchbase organization urls','usage':'?search= <search keyword>'},
            {'path':'/crunchbase_lookup','desc':'uses organization link as parameter to web scrap crunchbase','usage':'?search= <crunchbase organization link>'},
            {'path':'/smart_dump','desc':'using google scraping does a smart dump of all information on given symbol','usage':'?symbol= <symbol>'},
            
            {'path':'/symbol_lookup','desc':'symbol lookup using finnhub service','usage':'?search= <search keyword>'},
            {'path':'/symbol_lookup','desc':'symbol lookup using finnhub service','usage':'?search= <search keyword>'}
            
            ]
    })

@app.route('/symbol_lookup')
def symbol_lookup():
    _search = request.args.get('search')
    return json.dumps(finnhub_symbol_lookup(_search))

@app.route('/crunchbase_google_search')
def crunchbase_google_search():
    _search = request.args.get('search')
    response = requests.get(scrapy_crunchbase_google_server_endpoint(_search))
    return json.dumps(response.json())

#?search=<crunchbase organization link>
@app.route('/crunchbase_lookup')
def crunchbase_lookup():
    _search = request.args.get('search')
    response = requests.get(scrapy_crunchbase_server_endpoint(_search))
    return json.dumps(response.json())



@app.route('/googlefinance_lookup')
def googlefinance_lookup():
    _symbol = request.args.get('symbol')
    response = requests.get(scrapy_bist_google_scrap_endpoint(_symbol))
    return json.dumps(response.json())

@app.route('/bistprice_lookup')
def bistprice_lookup():
    _search = request.args.get('search')
    response = requests.get(scrapy_bist_google_finance_endpoint(_search))
    return json.dumps(response.json())


@app.route('/smart_dump')
def smart_dump():
    
    _symbol = request.args.get('symbol')
    result = {'crunchbase':[],'google':[],'finnhub': []}
    
    google_items = requests.get(scrapy_crunchbase_google_server_endpoint(_symbol)).json()['items']
    if len(google_items) > 0:
        for item in google_items[0]['links']:
            result['crunchbase'].append({'symbol':_symbol, 'crunchbase_data':requests.get(scrapy_crunchbase_server_endpoint(item)).json()['items']})
            
            
    google_finance_items = requests.get(scrapy_bist_google_scrap_endpoint(_symbol)).json()['items']
    
    if len(google_finance_items) > 0:
        for item in google_finance_items[0]['links']:
            result['google'].append({'symbol':_symbol, 'price':requests.get(scrapy_bist_google_finance_endpoint(item)).json()['items'][0]['price']})
            
    
    
    result['google'].append({
        'symbol':_symbol,
        'finnhub_company_profile':finnhub_company_profile(_symbol),
        'finnhub_company_peers':finnhub_company_peers(_symbol),
        'finnhub_company_basic_financials':finnhub_company_basic_financials(_symbol)
        })
    
    return json.dumps({'dump':result})

if __name__ == '__main__':
    app.run()