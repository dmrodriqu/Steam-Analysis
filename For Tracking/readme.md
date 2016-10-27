A series of scripts that

(initial run)
	pulls a large (just under 50k) sample of semi-random players from Steam who
		have public profiles
		logged into steam in the two weeks before the initial pull

(scheduled runs)
	pulls player*game level data on total time played on a 12 hour basis (steam limit = 100k, hence < 50k sample)
	this can provide
		general clustering information
		churn information on a per-game level (for games with decent sample size)
		transition rates between games

Files:

 all sql.sql
this file contains all sql used for the project
	initialization
	a few useful queries
	end analysis queries

 caller.py
this file contains the caller object that does the brunt of the work including
	making calls to steam api
	containing key, etc.

 initialPull.py
utilizes the caller object to collect a semi-random sample into a local sqlite3 db. 
Read steam documentation on userids. Assumptions:
	somewhat auto-incremented
Pulls:
	user, country, signup date, # friends

 scheduledPull.py
utilizes the caller object and the sqlite3 db to pull userids and make calls that collect user info

 pullScheduler.py
python script set up to run when my computer starts up. Every 15 minutes, checks log file. If log file was not updated since
the last 12 hour increment (gmt), runs scheduledPull.py's scheduledPull function. Else waits another 15 minutes.

 configs.py
any configs used across all the scripts. Imported for ease of change. Pretty lightweight.

 etc.
a file containing my steam api key exists in a folder above this hierarchy and is imported at runtime. 
Same for the .db file. If I publish any of this I plan to shared/upload the .db file. 