from urllib import request
import json, sqlite3, time, random
from caller import caller
from configs import dbName, keyLoc

class steam_id_maker:
    def __init__(self):
        self.base = 76561197960265728
        self.max = (76561198119092339-76561197960265728-1)/2
    def make_id(self):
        id_base = random.randint(1000, self.max)
        id_finished = id_base*2+1+self.base
        return str(id_finished)

#muh key
#instances
with open("../../key.txt", 'r') as keyFile:
    key = keyFile.read().strip()

c = caller(key, dbName)
idm = steam_id_maker()

count = 0 
while count < 95000:
    print(count)
    idstring = idm.make_id()
    for j in range(99):
        idstring = idstring + ","+ idm.make_id()
    try: count = count + c.getgameinfo_bootstrap(idstring)
    except: 
        print("Error Communicating With Host. Sleeping.")
        time.sleep(60)
#private ids return an empty result so check for that ish
#make account list and boostrap that ishhhh

#http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid=570
