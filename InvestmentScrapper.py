#Python 3.8.4
from email import header
from http import cookies
import json
import time

import calendar
import datetime
 
from jmespath import search
import requests

import finnhub
finnhub_client = finnhub.Client(api_key="cb6407qad3i70tu5u2tg")



def tickerAPI(symbol):
    response = requests.get(f"https://api.bitfinex.com/v1/pubticker/{symbol}")
    
    if(response.status_code == 200):
        return json.loads(response.text)
    else:
        print(response.text)
        return None
    
def tickerAPI_Symbols():
    response = requests.get("https://api.bitfinex.com/v1/symbols")
    
    if(response.status_code == 200):
        return json.loads(response.text)
    else:
        print(response.text)
        return None

def tickerAPI_Symbols():
    response = requests.get("https://api.bitfinex.com/v1/symbols_details")
    
    if(response.status_code == 200):
        return json.loads(response.text)
    else:
        print(response.text)
        return None
    
def vakifbank_bist():
    url  = "https://apigw.vakifbank.com.tr:8443/getBISTPrices"
    date = time.localtime(time.time())
    payload = {
        "SessionDate": f"{date.tm_year}-{date.tm_mon}-{date.tm_mday}T{date.tm_hour}:{date.tm_min}:{date.tm_sec}+03:00",
        "apikey":"l7xx2ea0bce246244b26b751440a8f9506d7"
    }
    
    header={"apikey":"l7xx2ea0bce246244b26b751440a8f9506d7"}
    cookies={"apikey":"l7xx2ea0bce246244b26b751440a8f9506d7"}
    
    print(payload)
    response = requests.post(url=url,data=payload,headers=header,cookies=cookies)
    
    if(response.status_code == 200):
        return json.loads(response.text)
    else:
        print(response.text)
        return None 

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
    finnhub_client.company_news(symbol)
    
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









