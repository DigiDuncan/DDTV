import os
import subprocess
import youtube_dl
import cv2
import time
import conf
import random

#Grab all possible videos 
videosinput = []
for root, dirs, files in os.walk(r'videos/'):
    for file in files:
        videosinput.append('videos/' + file)
for root, dirs, files in os.walk(r'commercials/'):
    for file in files:
        videosinput.append('commercials/' + file)

#Randomize video order
random.shuffle(videosinput)
        
#Pick a video to be played
queueposition = 0
currentshow = videosinput[queueposition]

#Video properties.
vid = cv2.VideoCapture(currentshow)
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
fcount = vid.get(cv2.CAP_PROP_FRAME_COUNT)
fps = vid.get(cv2.CAP_PROP_FPS)
length = fcount / fps

#Logo properties.
logoimage = 'custom/' + conf.logoimage
logofraction = 15 / conf.logosize #Logo size will be 1/logofraction of video width.
insetfraction = conf.insetfraction.split("/")
offsetdenominator = float(insetfraction[1]) #Logo will be set into the video by offsetnumerator/offsetdenominator pixels relative to video width.
offsetnumerator = offsetdenominator - float(insetfraction[0])
logosize = width / logofraction
pixelsoff = width - ((width / offsetdenominator) * offsetnumerator)
logox = width - pixelsoff - logosize
logoy = height - pixelsoff - logosize

print(f"FPS: {fps}\nFCOUNT: {fcount}\nLENGTH: {length}s ({length/60}m)")

#Play a video.
def mpv(passedfile):
    #Create mpv command.
    process = subprocess.Popen(f'mpv/mpv -fs -track-auto-selection= --lavfi-complex="[vid2] scale={logosize}:{logosize},format=rgba,colorchannelmixer=aa={conf.logoopacity} [logo],[vid1][logo] overlay=x={logox}:y={logoy} [vo]" {passedfile} --external-file={logoimage}',
    stdout=subprocess.PIPE)
    out, err = process.communicate()

    #Print mpv command results.
    print(out.decode("utf-8"))
    return(out.decode("utf-8"))

#Play the first video, and see if it exited on it's own.
output = mpv(currentshow)

#Exit code handling.
while True:
    if output.endswith("Exiting... (End of file)\r\n"): 
        queueposition = queueposition + 1
        currentshow = videosinput[queueposition]
        mpv(currentshow)
while True:    
    if output.endswith("Exiting... (Quit)"):
        os.system("taskkill /IM mpv.exe /F")