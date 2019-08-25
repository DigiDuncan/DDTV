import os

#Grab all possible videos from /videos directory
videosinput = []
for root, dirs, files in os.walk(r'videos/'):
	for file in files:
		videosinput.append('videos/' + file)

#Remove spaces from filenames
for i in range(len(videosinput)):
	if(videosinput[i].find(' ') != -1):
		os.rename(videosinput[i], videosinput[i].replace(' ', ''))