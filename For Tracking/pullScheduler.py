import time
from scheduledPull import scheduledPull
#Keeps a log file of pulls. If the last one was before the last 12 hour breakpoint, run a pull.

while(True):
	lastInterval = time.time() - time.time()%43200
	
	log = open('./pullLog.txt', 'r+')
	last = '0'
	tsLog = ''
	while len(last) > 0:
		tsLog = last
		last = log.readline().strip()

	if int(last) < lastInterval:
		log.write(str(time.time()))
		scheduledPull()

	#nighty night
	log.close()
	time.sleep(300)