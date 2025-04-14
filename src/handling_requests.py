import json
import requests
from handling_ui import *



def getData(url,address) -> tuple:
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
            motd: str = data["motd"]["clean"]
            mods = data["mods"]
            plugins = data["plugins"]
            player_list = []
            mods_list = []
            plugins_list = []
            max_player_list = 12
            try:
                for index in range(len(mods)):
                    mod = data["mods"][index]["name"]
                    mods_list.append(mod)
            except Exception as e:
                mods_list = []
                print("There was an error while loading the mods")
                print("DEBUG: ",e)
            if player_on < max_player_list:
                for index in range(player_on):
                    try:
                        player = data["players"]["list"][index]["name_clean"]
                        player_list.append(player)
                    except Exception:
                        player_list = []
                        print("DEBUG: There was an error while loading the player list")
            try:
                for index in range(len(plugins)):
                    plugin = data["plugins"][index]["name"]
                    plugins_list.append(plugin)
            except Exception as e:
                print("DEBUG: There was an error while loading the plugins.",e)
                plugins_list = []
            
            print(response.status_code)
        else:
            print(response.status_code)

    except Exception as e:
        print(e)
    return host,port,ip,eula,version,status,player_list,player_on,player_max,server_icon,motd,mods_list,plugins_list
    

