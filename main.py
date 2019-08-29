import os
import subprocess
import youtube_dl
import cv2
import time
import conf
import random
import datetime

#Load values from config.
logoimage = 'custom/' + conf.logoimage
logofraction = 15 / conf.logosize #Logo size will be 1/logofraction of video width.
insetfraction = conf.insetfraction.split("/")
offsetdenominator = float(insetfraction[1]) #Logo will be set into the video by offsetnumerator/offsetdenominator pixels relative to video width.
offsetnumerator = offsetdenominator - float(insetfraction[0])

#Get the properties of a video passed to this function.
def getVideoProperties(video):
    #Current video properties.
    vid = cv2.VideoCapture(video)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    fcount = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = vid.get(cv2.CAP_PROP_FPS)
    length = fcount / fps

    #Current logo properties.
    logosize = width / logofraction
    pixelsoff = width - ((width / offsetdenominator) * offsetnumerator)
    logox = width - pixelsoff - logosize
    logoy = height - pixelsoff - logosize

    return{"height": height, "width": width, "length": length, "logosize": logosize, "logox": logox, "logoy": logoy}

#Play a video.
def mpv(passedfile):
    #Update tracker.
    global currentfile
    currentfile = passedfile

    #Get video properties of current video.
    vp = getVideoProperties(passedfile)
    logosize, logox, logoy = vp["logosize"], vp["logox"], vp["logoy"]

    #Create mpv command.
    process = subprocess.Popen(f'mpv/mpv -fs -title="{conf.channelname}" -keep-open=yes --lavfi-complex="[vid2] scale={logosize}:{logosize},format=rgba,colorchannelmixer=aa={conf.logoopacity} [logo],[vid1][logo] overlay=x={logox}:y={logoy} [vo]" {passedfile} --external-file={logoimage}',
    stdout=subprocess.PIPE)
    out, err = process.communicate()

    #Print mpv command results.
    print(out.decode("utf-8"))
    return(out.decode("utf-8"))

#Constants.
now = datetime.datetime.now()
videosinput = commercialsinput = []
showlengths = comlengths = {}
print(now.minute)

#Trackers.
queueposition = 0
commercialqueueposition = 0
currentfile = ""

#Grab all "TV shows"
for root, dirs, files in os.walk(r'videos/'):
    for file in files:
        videosinput.append('videos/' + file)

#Grab all "commercials"
for root, dirs, files in os.walk(r'commercials/'):
    for file in files:
        commercialsinput.append('commercials/' + file)

#Calculate video lengths.
for file in videosinput:
    showlengths.update({file: getVideoProperties(file)["length"]})

#Randomize video order
random.shuffle(videosinput)
random.shuffle(commercialsinput)

#Pick a video to be played
currentshow = videosinput[queueposition]

#Exit code handling.
while True:
    print("Loop!")
    #Update time.
    now = datetime.datetime.now()
    #Play the current video.
    mpv(currentshow)
    print(getVideoProperties(currentfile)["length"])
