# import the necessary packages
from collections import deque
from turtle import st
from imutils.video import VideoStream
import numpy as np
import argparse
from scipy.spatial import distance as dist
from detect_obcopy import dist_in_pixel
import imutils
import cv2
import time
from threading import Timer
import timeit

#line a
ax=100
ay1=120
ay2=400
#line b
bx=500
by1=70
by2=400

pixdist_line = dist.euclidean((ax, ay1), (bx, by2)) ##400pix##distance of markers
print("Dist of lines in pixels"+str(pixdist_line))
vrdist = pixdist_line/dist_in_pixel #ratio of the amount of known objects to the line distance ## distance of object wihtin the frame  in ppm
##get distance between 2 lines then divide it by the ppm to get acutal distance in space
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())



def Speed_Cal(time):
    #Here i converted m to Km and second to hour then divison to reach Speed in this form (KM/H) 
    #the 9.144 is distance of free space between two lines # found in https://news.osu.edu/slow-down----those-lines-on-the-road-are-longer-than-you-think/
    #i know that the 9.144 is an standard and my video may not be that but its like guess and its need Field research
    try:
         #change time from ms to s
        Speed = (vrdist*dist_in_pixel)/(time)
        return Speed
    except ZeroDivisionError:
        print (5)

start_time = time.time()
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (0,0,139) #(102,31,75) (150,68,255)
greenUpper = (176,41,255)
pts = deque(maxlen=args["buffer"])
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["nball.mp4"])
# allow the camera or video file to warm up
time.sleep(2.0)


# keep looping
while True:
	# grab the current frame
	frame = vs.read()
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	#line a #i know road has got 
	#line a #i know road has got 
	cv2.line(frame,(ax,ay1),(ax,ay2),(255,0,0),2)
    #line b
	cv2.line(frame,(bx,by1),(bx,by2),(255,0,0),2)

	


		
# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 0:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			# update the points queue
			while int(ax) == int(x): ##while centroid is passing through the line sart time
					start_time = time.time()
					print("Timer Started")
					break
					
			while int(ax) <= int(x): #while ball is inbetween lines
				if int(bx) <= int(x) and int(bx+10) >= int(x): #if ball has just pased 2nd line or a little after make 2nd line green
					cv2.line(frame,(bx,by1),(bx,by2),(0,255,0),2)
					timetaken = time.time()-start_time
					print("Time taken"+str(timetaken))
					Speed = Speed_Cal(timetaken)
					print("Speed is :" + str(Speed) + "cm/s")
					time.sleep(1)
					print("Timer Cancel")
					end_time = 0
					start_time = 0
					print("End time and start reset:"+ str(end_time) +str(start_time))
					break
				else :
					cv2.putText(frame, "Calcuting", (100,200), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),3)
					break
	

	pts.appendleft(center)


	

# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
# otherwise, release the camera
else:
	vs.release()
# close all windowsQQQQQ
cv2.destroyAllWindows()