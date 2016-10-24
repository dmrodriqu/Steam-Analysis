from urllib import request
import json, sqlite3, time, random


#accounts active in last two weeks
#at least ~6mo old as of 2015-21-2015


#steam_base = 76561197960265728
#steam_max_num = (76561198119092339-76561197960265728-1)/2 #my smurf from ~sept's ID, deconstructed

class caller:
    def __init__(self, key, db):
        self.key = key
        self.conn = sqlite3.connect(db)

    def get_response(self, userid, domain, method, version):
        
        if(method == "GetPlayerSummaries"): idname = "&steamids="
        elif(method=="GetFriendList"): idname = "&relationship=friend&steamid=" 
        else: idname = "&steamid=" 

        url = "http://api.steampowered.com/" +\
        domain +\
        "/" +\
        method +\
        "/" +\
        version +\
        "/?key=" +\
        self.key +\
        idname +\
        userid +\
        "&format=json"
        response = request.urlopen(url)
        response_parsed = json.loads(response.read().decode('ascii', 'ignore'))
        return response_parsed

    def getgameinfo_update(self):
        #response_parsed = self.get_response(userid, "IPlayerService", "GetRecentlyPlayedGames", "v0001")
        #if 'games' in response_parsed:
        #    gamelist = response_parsed['response']['games']
        #    for g in gamelist:
        #        if g['appid'] == 570:
        #            print('ayy')
        ts = time.time()
        cur = self.conn.cursor()
        idlist = cur.execute('SELECT distinct pid from users').fetchall()
        ids = entry[0] for entry in idlist
        for this in ids:
            try:
                gamelist_parsed = self.get_response(this, "IPlayerService", "GetRecentlyPlayedGames", "v0001")   
                if('games' in gamelist_parsed['response']):
                    gamelist = gamelist_parsed['response']['games']
                    with self.conn:
                        cur = self.conn.cursor()
                        for g in gamelist:
                            cur.execute("INSERT INTO timeseries VALUES("+\
                                str(ts)+","+\
                                str(this)+","+\
                                str(g['appid'])+","+\
                                str(g['playtime_forever'])+")")
            except: print("Error updating " +str(this))

    def getgameinfo_bootstrap(self, userid):
        userinfo_parsed = self.get_response(userid, "ISteamUser", "GetPlayerSummaries", "v0002")
        #communityvisibilitystate = 3 means public,1 means private, need public. Record this.
        playerlist = userinfo_parsed['response']['players']
        testct = 0
        for p in playerlist:
            #public profile and on in the last week
            
            if p['communityvisibilitystate'] == 3 and 'lastlogoff' in p and time.time() - p['lastlogoff'] <= 1209600:
                #user info
                testct = testct + 1
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
                        cur.execute("INSERT INTO friends VALUES ("+\
                            str(thisid)+","+\
                            str(f['steamid'])+","+\
                            str(f['friend_since'])+")")
   #print("ID: "+str(friend_id) + " Timer: "+str(friend_time))
                    cur.execute("INSERT INTO users VALUES("+\
                        str(thisid)+","+\
                        str(friend_count)+",'"+\
                        str(country)+"',"+\
                        str(p['timecreated'])+")")

                #game list
                with self.conn:
                    cur = self.conn.cursor()
                    #recent games
                    gamelist_parsed = self.get_response(thisid, "IPlayerService", "GetRecentlyPlayedGames", "v0001")
                    if('games' in gamelist_parsed['response']):
                        gamelist = gamelist_parsed['response']['games']
                        for g in gamelist:
                            cur.execute("INSERT INTO base_games VALUES("+\
                                str(thisid)+","+\
                                str(g['appid'])+","+\
                                str(g['playtime_2weeks'])+","+\
                                str(g['playtime_forever'])+")")
                    #or recently played (last two weeks)
        return testct


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
c = caller("2B287E0CA6E57C7D4671FAF310CA707A", 'Comp.db')
idm = steam_id_maker()

count = 0 
while count < 75000:
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
