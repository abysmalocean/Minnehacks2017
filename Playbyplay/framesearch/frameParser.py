# USAGE
# python save_key_events.py --output output

# import the necessary packages
from keyclipwriter import KeyClipWriter
#from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
#import numpy as np
import os
import subprocess
subprocess.run("./clear.sh")
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to output directory")
ap.add_argument("-v", "--video", required=True,
	help="path to video directory")
ap.add_argument("-f", "--fps", type=int, default=29.97,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="MJPG",
	help="codec of output video")
ap.add_argument("-b", "--buffer-size", type=int, default=64,
	help="buffer size of video clip writer")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to
# warmup
videoPath = args["video"]
print("Analyzing video")
cap = cv2.VideoCapture(videoPath)



# initialize key clip writer and the consecutive number of
# frames that have *not* contained any action
kcw = KeyClipWriter(bufSize=args["buffer_size"])
frameBuffer = 0
frameCount = 0
# keep looping
stoppedClock = False
while True:

	ret, img = cap.read()

	if frameCount % 15 == 0:
		cv2.imwrite("./frames/frame%d.png" % frameCount, img)
		proc = subprocess.getoutput("./getShotClock.sh ./frames/frame%d.png" % frameCount)
		#shotTimer = int(proc)
		try:
			shotTimer = int(proc)
		except:
			ValueError
			shotTimer = 30
		#print(shotTimer, ":", frameCount)
		fData = open("fData.txt", "a+")
		writeStr = (str(frameCount) + ":" + str(shotTimer) + "\n")
		fData.write(writeStr)
		fData.close()
		if (shotTimer == 30):
			stoppedClock = True
		else:
			stoppedClock = False
			frameBuffer = 0



	# if not recording and clock not stopped, start recording
	if kcw.recording == False and stoppedClock == False:
		timestamp = datetime.datetime.now()
		p = "{}/{}.avi".format(args["output"],
			timestamp.strftime("%Y%m%d-%H%M%S"))
		kcw.update(img)
		kcw.start(p, cv2.VideoWriter_fourcc(*args["codec"]),
				args["fps"])

	kcw.update(img)

	# otherwise, no action has taken place in this frame, so
	# increment the number of frameBufferutive frames that contain
	# no action
	if stoppedClock:
		frameBuffer += 1

	# update the key frame clip buffer


	# if we are recording and reached a threshold on consecutive
	# number of frames with no action, stop recording the clip
	if kcw.recording and frameBuffer >= args["buffer_size"]:
		frameBuffer = 0
		kcw.finish()

	frameCount += 1
	print("Framebuffer: ",frameBuffer, "| Buffer_size: ", args["buffer_size"], " |Recording: ", kcw.recording, "| Shotclock :", shotTimer)
	# show the frame
	'''
	try:
		cv2.imshow("Frame", img)
	except:
		cv2.error
	'''
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# if we are in the middle of recording a clip, wrap it up
if kcw.recording:
	kcw.finish()

# do a bit of cleanup
cap.release()
cv2.destroyAllWindows()
