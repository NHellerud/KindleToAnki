import datetime
import time


def getTimeLeft(time, stopwatch, count, numberOfElements):
	###Returns the estimated time left
	###
	currentTime = time.time() - stopwatch
	estimatedTime = round(currentTime * (numberOfElements - count) / count)
	estimatedHours = int(estimatedTime / 3600)
	estimatedMinutes = int((estimatedTime - (estimatedHours * 3600)) / 60)
	estimatedSeconds = estimatedTime - (estimatedHours * 3600) - (estimatedMinutes * 60)
	estimatedTime = str(estimatedTime)
	if(estimatedHours < 10):
		estimatedHours = "0" + str(estimatedHours)
	else:
		estimatedHours = str(estimatedHours)

	if(estimatedMinutes < 10):
		estimatedMinutes = "0" + str(estimatedMinutes)
	else:
		estimatedMinutes = str(estimatedMinutes)

	if(estimatedSeconds < 10):
		estimatedSeconds = "0" + str(estimatedSeconds)
	else:
		estimatedSeconds = str(estimatedSeconds)
	return "Estimated Time Left : " + estimatedHours + ":" + estimatedMinutes + ":" + estimatedSeconds
