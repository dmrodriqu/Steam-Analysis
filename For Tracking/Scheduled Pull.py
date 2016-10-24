from urllib import request
import json, sqlite3, time, random
from caller import caller 
from configs import dbName, keyLoc

##you dirty dogs don't get to know my key!
with open(keyLoc, 'r') as keyFile:
    key = keyFile.read().strip()
c = caller(key, dbName)
c.getGames()
