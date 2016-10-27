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

	if float(tsLog) < lastInterval:
		log.write('\n')
		log.write(str(time.time()))
		log.close()
		print("Running a pull")
		scheduledPull()
		print("Pull Finished")
	else:
		print("Not ready to run a pull")
		log.close()
	#nighty night
	time.sleep(900)