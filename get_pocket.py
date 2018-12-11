#!/usr/bin/python

import requests

access_token = "xxx"
consumer_key = "xxxx"
get_url = 'https://getpocket.com/v3/get'
params = {'consumer_key': consumer_key, 'access_token': access_token, 'count': 1, 'detailType': 'simple'}

results = requests.get(get_url, params=params)
print(results.status_code)
data = results.json()
print(data)
print("\n")
print(data['list']['1941651579']['given_url'], data['list']['1941651579']['resolved_title'])



