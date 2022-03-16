import cv2
import numpy as np

cap = cv2.VideoCapture(0)
prevCircle =None
dist = lambda x1,y1,x2,y2: (x1-x2)^2+(y1-y2)^2




while True:
	ret, frame = cap.read()

	if not ret: break

	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) ##change to grayscale

	blurred_frame = cv2.GaussianBlur(gray, (17, 17), 0) #blur image to remove unwanted trackable balls
	circles = cv2.HoughCircles(blurred_frame,cv2.HOUGH_GRADIENT,1.2,100,
						param1=100,param2=30,minRadius=50,maxRadius = 100) #min dist is 100 bevcause we want to only find one circle since its the min dist,param 2 is the edge points
	
	if circles is not None: #circles list
		circles = np.uint16(np.around(circles)) #convert into in
		chosen = None
		for i in circles[ 0,:]: # this function find the next circle that is the most similar to the previous circle
			if chosen is  None: chosen = i
			if prevCircle is not None:
				if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1])<= dist(i[0],i[1],prevCircle[0],prevCircle[1]):
					chosen = i #if there is a circle that is closer ot the center point than the previous circle,than this is the new circle
			cv2.circle(frame, (chosen[0],chosen[1]), 1,  (0,100,100),3) #centerpoint
			cv2.circle(frame, (chosen[0], chosen[1]), chosen[2], (255,0,255,3), 3)
			prevCircle=chosen
	
	contours,_= cv2.findContours(frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	max_contour = contours[0]
	for contour in contours:
            if cv2.contourArea(contour)>cv2.contourArea(max_contour):

            	max_contour = contour

approx=cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
x,y,w,h=cv2.boundingRect(approx)
	cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),4)

        M=cv2.moments(contour)
		cx=int(M["m10"]//M["m00"])
		cy=int(M["m010"]//M["m00"])
		cv2.circle(frame, (cx,cy),3,(255,0,0),-1)

	cv2.imshow("circles",frame)



	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
    	
cap.release()
cv2.destroyAllWindows()
	