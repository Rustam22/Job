from __future__ import division
from datetime import datetime
import requests
from lxml import html, etree
import json
from textblob import TextBlob

import pandas as pd
from pprint import pprint

import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')


api_key = "AIzaSyBwQ6N1_r5r2UyT2LtQJgQbHtFjrtZl7w8"


pd.options.display.max_columns = 100
pd.options.display.max_rows = 35
pd.options.display.width = 120



#----------------Searching YouTube Using youtube.search.list---------------#

parameters = {
                "part": "snippet",
                "maxResults": 5,
                "order": "date",
                "pageToken": "",
                "publishedAfter": "2008-08-04T00:00:00Z",
                "publishedBefore": "2008-11-04T00:00:00Z",
                "q": "",
                "key": api_key,
                "type": "video",
              }

url = "https://www.googleapis.com/youtube/v3/search"
parameters['q'] = "Mark Udall"
page = requests.request(method="get", url=url, params=parameters)
j_results = json.loads(page.text)

#print page.text





#----------------YouTube Video Meta Data Using youtube.video.list---------------#
parameters = {"part": "statistics",
              "id": "WSKi8HfcxEk",
              "key": api_key,
              }
url = "https://www.googleapis.com/youtube/v3/videos"

page = requests.request(method="get", url=url, params=parameters)
j_results = json.loads(page.text)
#print page.text










