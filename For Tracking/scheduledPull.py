##you dirty dogs don't get to know my key!
def scheduledPull():
	from caller import caller 
	from configs import dbName, keyLoc
	with open(keyLoc, 'r') as keyFile:
	    key = keyFile.read().strip()
	c = caller(key, dbName)
	c.getGames()
