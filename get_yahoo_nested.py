import json
import requests
url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22milwaukee%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"

r = requests.get(url)
response_json = r.json()
print(response_json)
print("\n")

print(response_json['query']['results']['channel']['item']['condition']['temp'], response_json['query']['results']['channel']['unit
