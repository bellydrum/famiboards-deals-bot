#! /usr/bin/env python3

from datetime import datetime
import json
import requests
import tweepy
from pprint import pprint

from creds import *

now = datetime.now()


SALES_REPORT_FILEPATH = '/etc/apis/eshop-api/data/output/reports/salesReportPostText_1.txt'
LOG_FILENAME = '/etc/scripts/famiboards-deals-bot/logs/log-{}.txt'.format(now.strftime('%Y-%m-%d'))
LOG_FORMAT = '{} | {}: {}\n'
REQUEST_URL_FORMAT = "{}?order=post_date&direction=desc"

XF_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'XF-Api-Key': XF_API_KEY
}
XF_URL = "https://famiboards.com/api"

FORUMS = {
    2: 'Treehouse',
    8: 'The Roost',
    9: 'Community',
    14: 'Rustys Real Deals',
}

post_text = ''

with open(SALES_REPORT_FILEPATH, 'r') as f:
    print(f.read())

# response = requests.post(
#     XF_URL + '/threads/?node_id=14&title="hey, test!"&message=this is a test...&discussion_open=true',
#     headers=XF_HEADERS,
# ).json()
# pprint(response)