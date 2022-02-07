#! /usr/bin/env python3

import os

from datetime import datetime
import json
import requests
import tweepy
from pprint import pprint

from creds import *

now = datetime.now()

SALES_REPORT_FILEPATH = '/etc/apis/eshop-api-node/data/output/reports/'
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

# get all sales report files - US and EU
sales_report_files = os.listdir(SALES_REPORT_FILEPATH)
sales_report_files_us = [i for i in sales_report_files if 'america' in i.lower()]
sales_report_files_eu = [i for i in sales_report_files if 'europe' in i.lower()]

# generate and post US sales thread
if len(sales_report_files_us) > 0:

    URL = XF_URL + '/threads/'
    THREAD_TITLE = "NA eShop Deals Roundup | {}".format(now.strftime('%m-%d-%Y'))
    POST_TEXT = ''

    if len(sales_report_files_us) == 1:

        filepath = SALES_REPORT_FILEPATH + sales_report_files_us[0]
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
        print('There are {} sales report files.'.format(len(sales_report_files_us)))

        THREAD_BODY_FILEPATH = SALES_REPORT_FILEPATH + sales_report_files_us[0]
        THREAD_POST_FILES = sales_report_files_us[1:]

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
    print('There are currently no US sales report files.')


# generate and post EU sales thread
if len(sales_report_files_eu) > 0:

    # URL = XF_URL + '/threads/'
    # THREAD_TITLE = "EU eShop Deals Roundup | {}".format(now.strftime('%m-%d-%Y'))
    # POST_TEXT = ''
    #
    # if len(sales_report_files_eu) == 1:
    #
    #     filepath = SALES_REPORT_FILEPATH + sales_report_files_eu[0]
    #     with open(filepath, 'r') as f:
    #         POST_TEXT = f.read()
    #
    #     response = requests.post(
    #         URL,
    #         headers=XF_HEADERS,
    #         data={
    #             "node_id": 14,
    #             "title": THREAD_TITLE,
    #             "message": POST_TEXT,
    #             "discussion_open": True,
    #         }
    #     ).json()
    # else:
    #     print('There are {} sales report files.'.format(len(sales_report_files_eu)))
    #
    #     THREAD_BODY_FILEPATH = SALES_REPORT_FILEPATH + sales_report_files_eu[0]
    #     THREAD_POST_FILES = sales_report_files_eu[1:]
    #
    #     with open(THREAD_BODY_FILEPATH, 'r') as f:
    #         POST_TEXT = f.read()
    #
    #     response = requests.post(
    #         URL,
    #         headers=XF_HEADERS,
    #         data={
    #             "node_id": 14,
    #             "title": THREAD_TITLE,
    #             "message": POST_TEXT,
    #             "discussion_open": True,
    #         }
    #     )
    #     new_thread_id = response.json()['thread']['thread_id']
    #     print('New thread id: ' + str(new_thread_id))
    #
    #     for file in THREAD_POST_FILES:
    #         with open(SALES_REPORT_FILEPATH + file, 'r') as f:
    #             POST_TEXT = f.read()
    #         requests.post(
    #             XF_URL + '/posts/',
    #             headers=XF_HEADERS,
    #             data={
    #                 "thread_id": new_thread_id,
    #                 "message": POST_TEXT,
    #             }
    #         )
    pass

else:
    print('There are currently no EU sales report files.')
