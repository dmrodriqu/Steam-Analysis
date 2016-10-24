from urllib import request
import json, sqlite3, time, random

class caller:
    def __init__(self, key, dbName):
        self.key = key
        self.conn = sqlite3.connect(dbName)

    def getResp(self, userId, domain, version):

        if(method == "GetPlayerSummaries"): idName = "&steamids="
        elif(method=="GetFriendList"): idName = "&relationship=friend&steamid=" 
        else: idName = "&steamid=" 

        url = "http://api.steampowered.com/" +\
            domain +\
            "/" +\
            method +\
            "/" +\
            version +\
            "/?key=" +\
            self.key +\
            idName +\
            userId +\
            "&format=json"
        resp = request.urlopen(url)
        parsedResp = json.loads(resp.read().decode('ascii', 'ignore'))
        return parsedResp

    def getGames(self):
        ts = time.time()
        cursor = self.conn.cursor()
        idlist = cursor.execute('SELECT pid from users').fetchall()
        ids = entry[0] for entry in idlist
        # just pulled all the ids from our id list. Steam chokes @100k calls a day so we'll do 30k x 3
        for userId in ids:
            try:
                gamelist_parsed = self.getResp(userId, "IPlayerService", "GetOwnedGames", "v0001")   
                if('games' in gameListParsed['response']):
                    gameList = gameListParsed['response']['games']
                    with self.conn:
                        cur = self.conn.cursor()
                        for g in gameList:
                            cur.execute("INSERT INTO timeseries VALUES("+\
                                str(ts)+","+\
                                str(userId)+","+\
                                str(g['appid'])+","+\
                                str(g['playtime_forever'])+")")
            except: print("Error updating " + str(userId))

    def getUsers(self, userIds):
        userinfo_parsed = self.get_response(userIds, "ISteamUser", "GetPlayerSummaries", "v0002")
        #communityvisibilitystate = 3 means public,1 means private, need public. Record this.
        playerlist = userinfo_parsed['response']['players']
        testct = 0
        for p in playerlist:
            testct = testct + 1
            if p['communityvisibilitystate'] == 3 and 'lastlogoff' in p and time.time() - p['lastlogoff'] <= 1209600:
                #user info
                thisid = p['steamid']
                
                if 'loccountrycode' in p:
                    country = p['loccountrycode']
                else:
                    country = ''
                #friend list
                friendlist_parsed = self.get_response(thisid, "ISteamUser", "GetFriendList", "v0001")
                friendlist = friendlist_parsed['friendslist']['friends']
                friend_count = 0
                with self.conn:
                    cur = self.conn.cursor()
                    for f in friendlist:
                        friend_count = friend_count + 1

                    cur.execute("INSERT INTO users VALUES("+\
                        str(thisid)+","+\
                        str(friend_count)+",'"+\
                        str(country)+"',"+\
                        str(p['timecreated'])+")")

        #so we don't go over the steam call limit when collecting info
        return testct
