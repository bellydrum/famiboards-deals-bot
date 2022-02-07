#! /usr/bin/env python3

import os

from datetime import datetime
import json
import requests
import tweepy
from pprint import pprint

from creds import *

now = datetime.now()

SALES_REPORT_FILEPATH = '/etc/apis/eshop-api/data/output/reports/'
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

sales_report_files = os.listdir(SALES_REPORT_FILEPATH)

if len(sales_report_files) > 0:

    THREAD_TITLE = "Rusty's Sales Roundup | {}".format(now.strftime('%m-%d-%Y'))

    post_text = ''

    if len(sales_report_files) == 1:
        print('There is only one sales report file.')
        url = XF_URL + f'/threads/?node_id=14&title=f{0}&message={1}&discussion_open=true'.format(
            THREAD_TITLE, post_text
        )
        print(url)
        response = requests.post(
            XF_URL + '/threads/?node_id=14&title={title}&message={post_text}&discussion_open=true'.format(
                THREAD_TITLE, post_text
            ),
            headers=XF_HEADERS
        ).json()
        pprint(response)
    else:
        print('There are {} sales report files.'.format(len(sales_report_files)))
else:
    print('There are currently no sales report files.')
