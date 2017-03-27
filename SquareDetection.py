### Sources
## http://stackoverflow.com/questions/35042254/shape-detection-using-opencv-from-live-video-stream?noredirect=1&lq=1
## https://github.com/opencv/opencv/blob/master/samples/python/squares.py

import cv2
import numpy as np
import sys

cap = cv2.VideoCapture(0)
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )
	
def find_squares(vid):
	vid = cv2.GaussianBlur(vid, (5, 5), 0)
	squares = []
	for gray in cv2.split(vid):
		for thrs in xrange(0, 255, 26):
			if thrs == 0:
				edge = cv2.Canny(gray, 0, 50, apertureSize=5)
				edge = cv2.dilate(edge, None)
			else:
				retval, edge = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
			edge, contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			
			for cnt in contours:
				cnt_len = cv2.arcLength(cnt, True)
				cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
				if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
					cnt = cnt.reshape(-1, 2)
					max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
					if max_cos < 0.1:
						squares.append(cnt)
	return squares

"""def find_altitude(squares): TODO
	squareFloorDimension=1 ## 1m
	pointA=squares[0][0] ## position of the square point
	pointB=squares[0][1]
	pointC=squares[0][2]
	pointD=squares[0][3]
	AB=squares[0][1]-squares[0][0] ## dimensions of the square detected
	BC=squares[0][2]-squares[0][1]
	CD=squares[0][3]-squares[0][2]
	DA=squares[0][0]-squares[0][3]
	# k= ? (we have to find it)
	altitude= k*AB/squareFloorDimension ## if altitude=0 ==> AB=1
	## Example: If the drone sees a square of 50cm and we know that the square measures 1m we can find the altitude?
	
	return altitude"""

while(True):	
	ret, frame = cap.read()
	squares = find_squares(frame)
	#print(find_altitude(squares))
	cv2.imshow("frame", frame)
	cv2.drawContours(frame, squares, -1, (0, 255, 0), 3 )
	cv2.imshow('squares', frame)
	k = cv2.waitKey(60) &0xFF
	if k == 27:
		cap.release()
		cv2.destroyAllWindows()
		break
		
#Note: Find a way to calculate the altitude by calculate the dimension of the square in the frame