#!/usr/bin/python

import requests, json, datetime


access_token = "xxxx"
consumer_key = "xxxx"
post_url = 'https://getpocket.com/v3/add'
since = int(datetime.datetime.now().strftime("%s")) - 86400
data = {'url': 'https://tutorialedge.net/python/create-rest-api-python-aiohttp/',
        'consumer_key': consumer_key,
        'access_token': access_token
        }





pocket_add = requests.post(post_url, data=data)
pocket_add.status_code
