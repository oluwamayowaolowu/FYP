"""
Filename: init.py
Usage: This script will measure different objects in the frame using a reference object of known dimension. 
The object with known dimension must be the leftmost object.
Author: Shashank Sharma
"""
from inspect import currentframe
from scipy.spatial.distance import euclidean
from sympy import re
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import os 
from PIL import Image
import glob



vidcap = cv2.VideoCapture(0) #open webcam

ret,frame = vidcap.read()
currentframe =0
while(True):
	if ret:
		name = '\frames('+str(currentframe)+').jpg'
		cv2.imwrite(name,frame)  
		currentframe = currentframe+1
	if (currentframe == 50):
		break
	else:
		break






img_path = "frame(10).jpg"

orangeLower = (172,81,69) # red candle(0,174,77)(179,231,146)
orangeUpper = (179,255,248)

# Read image and preprocess
image = cv2.imread(img_path)

image = imutils.resize(image, width=640)
blurred = cv2.GaussianBlur(image,(11,11),0)
hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, orangeLower, orangeUpper)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)


#show_images([blur, edged])

# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(mask, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
# find contours in the edge map


# Find contours
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)


# Remove contours which are not large enough
cnts = [x for x in cnts if cv2.contourArea(x) > 100]

#cv2.drawContours(image, cnts, -1, (0,255,0), 3)

#show_images([image, edged])
#print(len(cnts))

# Reference object dimensions
# Here for reference I have used a 2cm x 2cm square
ref_object = cnts[0]
box = cv2.minAreaRect(ref_object)
box = cv2.boxPoints(box)
box = np.array(box, dtype="int")
box = perspective.order_points(box)
(tl, tr, br, bl) = box
dist_in_pixel = euclidean(tl, tr)
print("Distance of ref object in pixels is " + str(dist_in_pixel))
dist_in_cm = 8
pixel_per_cm = dist_in_pixel/dist_in_cm

# Draw remaining contours
for cnt in cnts:
	box = cv2.minAreaRect(cnt)
	box = cv2.boxPoints(box)
	box = np.array(box, dtype="int")
	box = perspective.order_points(box)
	(tl, tr, br, bl) = box
	cv2.drawContours(image, [box.astype("int")], -1, (0, 0, 255), 2)
	mid_pt_horizontal = (tl[0] + int(abs(tr[0] - tl[0])/2), tl[1] + int(abs(tr[1] - tl[1])/2))
	mid_pt_verticle = (tr[0] + int(abs(tr[0] - br[0])/2), tr[1] + int(abs(tr[1] - br[1])/2))
	wid = euclidean(tl, tr)/pixel_per_cm
	ht = euclidean(tr, br)/pixel_per_cm

	cv2.putText(image, "{:.1f}cm".format(wid), (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)), 
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
	cv2.putText(image, "{:.1f}cm".format(ht), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])), 
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

# Function to show array of images (intermediate results)

	cv2.imshow("image_" , image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

