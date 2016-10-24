-- command prompt level
sqlite3 SteamAnalysis

-- setup commands
create table userlist (
	user_id varchar(100)
	,friend_count int 
	,country varchar(100)
	,created timestamp
)

create table user_game (
	user_id
	,game_id
	,inserted timestamp
	,time_played
)