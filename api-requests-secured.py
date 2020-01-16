import requests
import json
import pprint
import configparser

config = configparser.ConfigParser()
config.read('secrets.ini')
myusername = config['auth']['username']
mypassword = config['auth']['password']

api_key = "XXXXX"
zone_id = "XXXX"
account_id = "XXXX"
tsig_secret_name = "XXXXXX"
tsig_secret_string = "XXXXX"
tsig_id = "XXXXXXXX"
algo = "hmac-md5"
master_ip = "XXXXXXX"
proxy_host = "XXXXXXXXXXX"
proxy_port = "XXXXX"
proxy_auth = ("{}:{}".format(myusername, mypassword))

proxies = {
       "https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
       "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)
}

def verify_access():
    url = "https://XXXXXXXXXXXXXXXX"

    headers = {
        'Authorization': "Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        'Host': "XXXXXXXXXXXXXX",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, proxies=proxies, headers=headers)

    if (response.status_code == 200) or (response.status_code == 201):
        print("SUCCESSFUL! status code: {}".format(response.status_code))
        pprint.pprint(response.json())
    else:
        print("ERROR! status code: {} Reason: {}".format(response.status_code, response.reason))

def create_slave_zone():
	pass


def configure_tsig():
    pass

def add_master_zone():
    pass

def integrate_master_zone():
    pass



if __name__ == "__main__":
    #verify_access()
    create_slave_zone()

