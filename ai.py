import cv2 
import numpy as np
import time
import os

from arduino import Arduino
# ARDUINO_PORT = '/dev/ttyUSB0'
# arduino = Arduino(ARDUINO_PORT, baudrate=115200, timeout=10)
# time.sleep(1)

import pigpio



os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(2)


ESC = 17 
STEER = 18 

pi = pigpio.pi()
time.sleep(2)

print("podau signal")

pi.set_servo_pulsewidth(STEER, 1400)
time.sleep(2)



SIZE = (400, 300)



RECT = np.float32([[0, 299],
                   [399, 299],
                   [399, 0],
                   [0, 0]])



TRAP = np.float32([[30, 250],  
                   [350, 250],  
                   [330, 200] , #order is important 
                   [50, 200], 
                   

                      
                   ]) 




cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
name = 0

while True:
    
    ret, frame = cap.read()
    if not ret:
       print("End of File")
       break


    

    #frame_for_znak = copy.copy(frame)
    #znaki.detect_znak(frame_for_znak)

    
    resize = cv2.resize(frame, SIZE)
    cv2.imshow("frame", frame)

    
    

    cv2.circle(frame, (30, 250), 5, (0,0,255), -1)
    cv2.circle(frame, (50, 200), 5, (0,0,255), -1)

    cv2.circle(frame, (350, 250), 5, (0,0,255), -1)
    cv2.circle(frame, (330, 200), 5, (0,0,255), -1)


    cv2.imshow("frame", frame)
    # plt.imshow(frame)
    # plt.show()


    #frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    r_channel = resize[:,:,2]
    binary = np.zeros_like(r_channel)
    binary[(r_channel > 200)] = 1

    hls = cv2.cvtColor(resize, cv2.COLOR_BGR2HLS)
    s_channel = resize[:,:,2]
    binary2 = np.zeros_like(s_channel)
    binary2[(r_channel > 250)] = 1 #if road light we above 

    allBinary = np.zeros_like(binary)
    allBinary[(binary==1) | (binary2==1)] =255
    
    

    binary_visual = allBinary.copy()
    cv2.imshow("binary", binary_visual)

    
    cv2.polylines(binary_visual, [np.array(TRAP, dtype=np.int32)], True, 255, 2)
    M = cv2.getPerspectiveTransform(TRAP, RECT)
    perspective = cv2.warpPerspective(allBinary, M, SIZE, flags=cv2.INTER_LINEAR)
    
    #cv2.imshow("Perspective", perspective)
    

    hist = np.sum(perspective[0:200], axis=0) #axis
    
    center = hist.shape[0] // 2
    #print('center',center)

    hist_l = hist[:center]
    hist_r = hist[center:]
    #print(f" {hist_l=}")
    

    ind_left = np.argmax(hist_l)
    ind_right = np.argmax(hist_r) + center
    #print(ind_left, ind_right)

    out = perspective.copy()
    

    cv2.line(out, (ind_left, 0), (ind_left, 299), 255, 2)
    cv2.line(out, (ind_right, 0), (ind_right, 299), 255, 2)
    cv2.imshow("Lines", out)
    

    center_road = (ind_left + ind_right) // 2
    #print("center_road",center_road)
   

    Error = center_road - center
    #print('Error',Error)

    angle = 1400 + (Error * 10)
    print(angle)

    try:
        if angle in range(1400, 1800):
            pi.set_servo_pulsewidth(STEER, angle)
        
    except:
        pass





    k = cv2.waitKey(1)

    if k == ord("s"):
       # cv2.imwrite(f"foto/{name}.jpg", frame)
        name+=1

    elif k == ord("q"):
        break
