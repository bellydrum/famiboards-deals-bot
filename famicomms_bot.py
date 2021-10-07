#! /usr/bin/env python3

from datetime import datetime
import json
import requests
import tweepy

from creds import *

now = datetime.now()

''' API CREDS '''
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

LOG_FILENAME = '/etc/scripts/famicomms/logs/log-{}.txt'.format(now.strftime('%Y-%m-%d'))
LOG_FORMAT = '{} | {}: {}\n'
REQUEST_URL_FORMAT = "{}?order=post_date&direction=desc"
TWEET_FORMAT = '''{} posted a new thread in {}: 

"{}"
    
{}
'''

DATA_FILENAME = '/etc/scripts/famicomms/latest_post.json'

HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'XF-Api-Key': XF_API_KEY
}
URL = "https://famiboards.com/api/threads/?order=post_date&direction=desc"

FORUMS = {
    2: 'Treehouse',
    8: 'The Roost',
    9: 'Community'
}

try:
    api.verify_credentials()

    response = requests.get(URL, headers=HEADERS).json()
    latest_thread = response['threads'][0]

    latest_post = {
        'thread_id': latest_thread['thread_id'],
        'title': latest_thread['title'],
        'username': latest_thread['username'],
        'post_date': latest_thread['post_date'],
        'view_url': latest_thread['view_url'],
        'forum': FORUMS[latest_thread['node_id']]
    }

    with open(DATA_FILENAME) as f:
        latest_recorded_post_data = json.load(f)

    latest_recorded_post = latest_recorded_post_data

    if latest_post != latest_recorded_post:

        with open(DATA_FILENAME, 'w') as f:
            json.dump(latest_post, f)

        tweet = TWEET_FORMAT.format(
            latest_post['username'],
            latest_post['forum'],
            latest_post['title'],
            latest_post['view_url']
        )

        print(tweet)
        api.update_status(tweet)

except Exception as e:

    with open(LOG_FILENAME, 'a') as f:
        f.write(LOG_FORMAT.format(now, type(e), str(e)))