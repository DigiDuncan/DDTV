import os
import subprocess
import youtube_dl
import cv2
import time
import conf

inputfile = 'videos/' + 't4.mp4'

#Video properties.
vid = cv2.VideoCapture(inputfile)
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
fcount = vid.get(cv2.CAP_PROP_FRAME_COUNT)
fps = vid.get(cv2.CAP_PROP_FPS)
length = fcount / fps

#Logo properties.
logoimage = 'custom/' + conf.logoimage
logofraction = 15 / conf.logosize #Logo size will be 1/logofraction of video width.
offsetnumerator = 63
offsetdenominator = 64 #Logo will be set into the video by offsetnumerator/offsetdenominator pixels relative to video width.
logosize = width / logofraction
pixelsoff = width - ((width / offsetdenominator) * offsetnumerator)
logox = width - pixelsoff - logosize
logoy = height - pixelsoff - logosize


print(f"FPS: {fps}\nFCOUNT: {fcount}\nLENGTH: {length}s ({length/60}m)")

#Create mpv command.
process = subprocess.Popen(f'mpv/mpv -fs --lavfi-complex="[vid2] scale={logosize}:{logosize},format=rgba,colorchannelmixer=aa={conf.logoopacity} [logo],[vid1][logo] overlay=x={logox}:y={logoy} [vo]" {inputfile} --external-file={logoimage}',
    stdout=subprocess.PIPE)
out, err = process.communicate()

#Print mpv command results.
print(out.decode("utf-8"))
