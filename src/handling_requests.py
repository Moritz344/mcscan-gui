import json
import requests
from handling_ui import *



def getData(url,address):
    try:
        response = requests.get(url + address)
        if response.status_code == 200:
            data = response.json()

            host: str = data["host"]
            port: int = data["port"]
            ip:   str = data["ip_address"]
            eula: bool = data["eula_blocked"]
            version: str= data["version"]["name_clean"]
            status: bool = data["online"]

            print(response.status_code)
        else:
            print(response.status_code)

    except Exception as e:
        print(e)
    
    return host,port,ip,eula,version,status
    

