import json
import requests
from handling_ui import *



def getData(url,address):
    try:
        response = requests.get(url + address)
        if response.status_code == 200:
            print("DEBUG:",url + address)
            print(response.status_code)
        else:
            print("DEBUG:",url)
            print(response.status_code)

    except Exception as e:
        print(e)

    

