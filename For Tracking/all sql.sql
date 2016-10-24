-- command prompt
sqlite3 ../../../SteamAnalysis.db

-- setup commands
-- sqlite ints are huge...
create table users (
	user_id integer
	,friend_count integer
	,country varchar(20)
	,created integer
);
create table user_games (
	user_id integer 
	,game_id integer
	,inserted numeric
	,time_played integer
);