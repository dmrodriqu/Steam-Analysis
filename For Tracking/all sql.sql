-- command prompt
sqlite3 ../../../SteamAnalysis.db

-- setup commands
-- sqlite ints are huge...
/*
create tables for user information pertinent to userIDs, 
friend count, country of residence, and unix epoch when created
*/
create table users (
	user_id integer
	,friend_count integer
	,country varchar(20)
	,created integer
);

/*
create tables for user information pertinent to userIDs, 
numeric ID of game, ??order of purchase??, number of times played 
in unix epoch for each game
*/
create table user_games (
	user_id integer 
	,game_id integer
	,inserted numeric
	,time_played integer
);

--delete duplicates

/*
Selecting distinct user_id. 
Better performance than using "select distinct user_id from users".
O(n) should be --> linear time
*/
delete from users 
where user_id in 
	(
		/*
		Selecting from the newly created user_id table with
		the ct column. Any row with column ct>1 will be delted
		*/
		select 
			user_id
		from 
		(
			/*
			Selecting from user table, create a new column
			that counts instances called ct.
			*/
			select 
				user_id
				,count(*) as ct
			from users
			group by user_id
		)
		where ct > 1
	)
;

--export copy of userlist (just in case)
.headers on 
.mode csv
.output userlist.csv
select * from users;
