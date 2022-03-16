import numpy as np
import cv2
from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte

def resize(img):
   return cv2.resize(img,(512,512)) # arg1- input image, arg- output_width, output_height

cap=cv2.VideoCapture("roryswing.mp4")
ret,frame=cap.read()

l_b=np.array([180,1,99])# lower hsv bound for red
u_b=np.array([129,15,53])# upper hsv bound to red


while ret==True:
    ret,frame=cap.read()
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask=cv2.inRange(gray,200,255)

    #DETECT EDGES
    edges = canny(frame, sigma=3, low_threshold=10, high_threshold=50)
    #detect radius
    hough_radii = np.arange(20, 35, 1)
    hough_res = hough_circle(edges, hough_radii)

    # Select the most prominent 3 circles
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                           total_num_peaks=1)




    contours,_= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    max_contour = contours[0]
    for contour in contours:
      if cv2.contourArea(contour)>cv2.contourArea(max_contour):

        max_contour=contour
    
    contour=max_contour
    approx=cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
    x,y,w,h=cv2.boundingRect(approx)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),4)




    cv2.imshow("frame",resize(frame))

    cv2.imshow("mask",mask)


    key=cv2.waitKey(1)
    if key==ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows



planets	= cv2.imread('rory3.png')
gray_img	=	cv2.cvtColor(planets,	cv2.COLOR_BGR2GRAY)
img	= cv2.medianBlur(gray_img,	5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

rows = gray_img.shape[0]
circles	= cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,0.9,rows /8,param1 =100,param2=30,minRadius=9,maxRadius=0)
circles	= np.uint16(np.around(circles))
 
for	i in circles[0,:]:
				#	draw	the	outer	circle
				cv2.circle(planets,(i[0],i[1]),i[2],(0,255,0),6)
				#	draw	the	center	of	the	circle
				cv2.circle(planets,(i[0],i[1]),2,(0,0,255),3)
 
cv2.imshow("HoughCirlces",	planets)
cv2.waitKey()
cv2.destroyAllWindows()
