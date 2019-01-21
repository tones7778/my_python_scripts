#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import pprint
import configparser
import urllib3
urllib3.disable_warnings()

config = configparser.ConfigParser()
config.read('secrets.ini')


consumer_key = config['pocket']['consumer_key']
access_token = config['pocket']['access_token']
uri = 'https://getpocket.com/v3/get'
parameters = {"consumer_key": consumer_key, "access_token": access_token, "count": 10}
payload = ""

response = requests.get(uri, params=parameters, verify=False)

myjson = response.json()
pprint.pprint(response.status_code)
pprint.pprint(myjson)
