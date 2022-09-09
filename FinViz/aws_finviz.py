# from FinViz.finviz_webscraper import get_top_gainers2
import boto3
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import requests
from requests import get
import pandas as pd
import numpy as np
from time import sleep
import datetime
from datetime import date
import pytz

def page_amounts(url):
  req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  webpage = urlopen(req).read()
  html = soup(webpage, "html.parser")
  page_count = html.find_all(attrs = {'class': 'screener-pages'})

  p_count = 1
  for i in page_count:
    p_count += 1
  return p_count

def pages(page_url, page_number):
  top_gainers = []
  pages = np.arange(1, ((page_number * 20) + 1), 20)
  for page in pages:
    url = (page_url +"&r=" + str(page))
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    html = soup(webpage, "html.parser")

    gainers = html.find_all(attrs = {'class': 'screener-link-primary'})
    for ticker in gainers:
      top_gainers.append(ticker.get_text().strip())
    sleep(2) #so we can get all pages every single time
  return top_gainers

def get_top_gainers2(url, top_gainers):
  p_count = page_amounts(url)
  top_gainers = pages(url, p_count)
  return top_gainers

def main():
#######################################   
    # DATA_BUCKET = "finviz-daily-topgainers"
    # s3 = boto3.resource("s3")
    # bucket = s3.Bucket(DATA_BUCKET)
#######################################    
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    today = utc_now.astimezone(pytz.timezone("America/Chicago"))
    new_today = today.strftime("%m-%d-%Y")
    filename = 'top_gainers_' + new_today + '.csv'
    # filename = 'top_gainers_' + new_today + '.txt'
#######################################
    top_gainers = []
    get_top_gainers2("https://finviz.com/screener.ashx?v=110&s=ta_topgainers", top_gainers)
    print(top_gainers)
#######################################
    # s3.Object(DATA_BUCKET, filename).put(Body=top_gainers)
#######################################
    # with open(filename, 'w') as f:
    #     f.write(top_gainers)    

if __name__ == "__main__":
    main()