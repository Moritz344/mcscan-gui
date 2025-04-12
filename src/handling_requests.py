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
            server_icon: str = data["icon"]
            player_on: int = data["players"]["online"]
            player_max: int = data["players"]["max"]
            player_list = []
            max_player_list = 12
            
            if player_on < max_player_list:
                for index in range(player_on):
                    try:
                        player = data["players"]["list"][index]["name_clean"]
                        player_list.append(player)
                    except Exception:
                        player_list = []
                        print("DEBUG: There was an error while loading the player list")
    
            print(response.status_code)
        else:
            print(response.status_code)

    except Exception as e:
        print(e)
    return host,port,ip,eula,version,status,player_list,player_on,player_max,server_icon
    

