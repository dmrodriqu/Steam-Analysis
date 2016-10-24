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
with open(keyLoc, 'r') as keyFile:
    key = keyFile.read().strip()

#initialize caller object, and the (super hacky) steam id maker
c = caller(key, dbName)
idm = steam_id_maker()

#this is SUPER hacky and probably the biggest methodological hole here.
#Trying to make quasi random steam ids of a certain age, and see if they're set to be public
count = 0
lastCount = 0 
#don't go over call limit (steam = 100k/day)
while count < 99000:
    idstring = idm.make_id()
    for j in range(99):
        idstring = idstring + ","+ idm.make_id()
    try: count = count + c.getUsers(idstring) + 1 #1 for pull of list - then for every user that worked, 1 pull for their friendslist
    except: 
        print("Error Communicating With Host. Sleeping.")
        time.sleep(60)
    if count > lastCount + 100:
        lastCount = lastCount + 100
        print(count)



#http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid=570
