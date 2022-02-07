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

    URL = XF_URL + '/threads/'
    THREAD_TITLE = "NA eShop Deals Roundup | {}".format(now.strftime('%m-%d-%Y'))
    POST_TEXT = 'This is a test. [B]It works![/B]'

    if len(sales_report_files) == 1:

        filepath = SALES_REPORT_FILEPATH + sales_report_files[0]
        with open(filepath, 'r') as f:
            POST_TEXT = f.read()

        response = requests.post(
            URL,
            headers=XF_HEADERS,
            data={
                "node_id": 14,
                "title": THREAD_TITLE,
                "message": POST_TEXT,
                "discussion_open": True,
            }
        ).json()
    else:
        print('There are {} sales report files.'.format(len(sales_report_files)))

        THREAD_BODY_FILEPATH = SALES_REPORT_FILEPATH + sales_report_files[0]
        THREAD_POST_FILES = sales_report_files[1:]

        with open(THREAD_BODY_FILEPATH, 'r') as f:
            POST_TEXT = f.read()

        response = requests.post(
            URL,
            headers=XF_HEADERS,
            data={
                "node_id": 14,
                "title": THREAD_TITLE,
                "message": POST_TEXT,
                "discussion_open": True,
            }
        )
        new_thread_id = response.json()['thread']['thread_id']
        print('New thread id: ' + str(new_thread_id))

        for file in THREAD_POST_FILES:
            with open(SALES_REPORT_FILEPATH + file, 'r') as f:
                POST_TEXT = f.read()
            requests.post(
                XF_URL + '/posts/',
                headers=XF_HEADERS,
                data={
                    "thread_id": new_thread_id,
                    "message": POST_TEXT,
                }
            )

else:
    print('There are currently no sales report files.')
