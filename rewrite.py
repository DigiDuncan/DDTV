#TODO:
#Load videos
#Create playlist
#Overlay Logo
#Implement time slots

#Imports
import os
import subprocess
import youtube_dl
import cv2
import time
import rewriteconf
import random
import datetime

#Variables
videoDict = {}
commercialDict= {}

#Load values from config.
logoImage = 'custom/' + rewriteconf.logoImage
logoFraction = 15 / rewriteconf.logoSize #Logo size will be 1/logoFraction of video width.
insetFraction = rewriteconf.insetFraction.split("/")
offsetDenominator = float(insetFraction[1]) #Logo will be set into the video by offsetNumerator/offsetDenominator pixels relative to video width.
offsetNumerator = offsetDenominator - float(insetFraction[0])
enableCommercials = rewriteconf.enableCommercials

def normalizeFilenames(video):
	if(video.find(' ') != -1):
			os.rename(video, video.replace(' ', ''))

def loadVideos():
	#Shows/Movies
	for root, dirs, files in os.walk(r'videos/'):
		for file in files:
            path = 'videos/' + file
            normalizeFilenames(path)
			videoDict[path] = getVideoProperties(path)["length"]
	#Commericals
	if enableCommercials == True:
		for root, dirs, files in os.walk(r'commercials/'):
			for file in files:
                path = 'commercials/' + file
                normalizeFilenames(path)
				commercialDict[path] = getVideoProperties(path)["length"]

def getVideoProperties(video):
    #Current video properties.
    vid = cv2.VideoCapture(video)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    fcount = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = vid.get(cv2.CAP_PROP_FPS)
    length = fcount / fps

    #Current logo properties.
    logosize = width / logoFraction
    pixelsoff = width - ((width / offsetDenominator) * offsetNumerator)
    logox = width - pixelsoff - logosize
    logoy = height - pixelsoff - logosize

    return{"height": height, "width": width, "length": length, "logosize": logosize, "logox": logox, "logoy": logoy}

loadVideos()
