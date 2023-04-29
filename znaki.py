import cv2 
import numpy as np
import time
import os
import copy

noDrive = cv2.imread("nodrive.jpg")
pedestrian = cv2.imread("pedastrian.jpg")
right = cv2.imread("turn_right.jpg")

noDrive = cv2.resize(noDrive,(64,64))
pedestrian = cv2.resize(pedestrian,(64,64))
right = cv2.resize(right,(64,64))

noDrive = cv2.inRange(noDrive,(89,91,149), (255,255,255))
pedestrian = cv2.inRange(pedestrian,(89,91,149), (255,255,255))
right = cv2.inRange(right,(89,91,149), (255,255,255))

# cv2.imshow("noDrive", noDrive)
# cv2.imshow("pedestrian", pedestrian)



#cap = cv2.VideoCapture(0)



def detect_znak(frame_for_znak):


    frameCopy = copy.copy(frame_for_znak)

    hsv = cv2.cvtColor(frame_for_znak, cv2.COLOR_BGR2HSV)
    hsv = cv2.blur(hsv,(5,5))
    mask = cv2.inRange(hsv,(89,124,73),(255,255,255))
    cv2.imshow("Mask", mask)


    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=4)
    cv2.imshow("Mask2", mask)

    contours = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    contours = contours[0]
    if contours:
        contours = sorted(contours, key = cv2.contourArea, reverse=True)
        cv2.drawContours(frame_for_znak, contours,0,(255,0,255),3)
        cv2.imshow("contours", frame_for_znak)

        x,y,w,h = cv2.boundingRect(contours[0])
        cv2.rectangle(frame_for_znak, (x,y), (x+w, y+h), (0,255,0),2)
        cv2.imshow("Rect", frame_for_znak)

        roImg = frameCopy[y:y+h, x:x+w]
        cv2.imshow("Detect", roImg)

        roImg = cv2.resize(roImg,(64,64))
        roImg = cv2.inRange(roImg,(89,91,149), (255,255,255))
        cv2.imshow("Resized", roImg)


        noDrive_val = 0
        pedestrian_val = 0
        right_val = 0

        for i in range(64):
            for j in range(64):

                if roImg[i][j] == noDrive[i][j]:
                    noDrive_val +=1
                if roImg[i][j] == pedestrian[i][j]:
                    pedestrian_val+=1
                if roImg[i][j] == right[i][j]:
                    right_val+=1
        #print(f" {pedestrian_val=}")

        if pedestrian_val in range(3100, 3500):
            print("pedestrian")
        # elif noDrive_val > 2000:
        #     print("nodrive")
        # elif right_val in range(2100, 2300):
        #     print("right")

    
    