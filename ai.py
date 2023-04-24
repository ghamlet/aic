import cv2 

import numpy as np
import time
import os
import pigpio


os.system("sudo pigpiod")  # Launching GPIO library


ESC = 17 
STEER = 18 

pi = pigpio.pi()

time.sleep(2)
print("podau signal")
pi.set_servo_pulsewidth(ESC, 1400)
time.sleep(2)



ESCAPE = 27
key = 1

SIZE = (400, 300)



RECT = np.float32([[0, 299],
                   [399, 299],
                   [399, 0],
                   [0, 0]])



TRAP = np.float32([[70, 250],     
                   [330, 250],  

                   [280, 200],   
                   [100, 200]]) 




cap = cv2.VideoCapture(0)


while True:
    
    ret, frame = cap.read()
    cv2.waitKey(1)

    if ret == False:
       print("End of File")
       break

    
    frame = cv2.resize(frame, SIZE)

    cv2.circle(frame, (140, 200), 5, (0,0,255), -1)
    cv2.circle(frame, (240, 200), 5, (0,0,255), -1)

    cv2.circle(frame, (70, 250), 5, (0,0,255), -1)
    cv2.circle(frame, (330, 250), 5, (0,0,255), -1)

    #cv2.imshow("frame", frame)
    
    

    
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Gray", frame_gray)

    

    binary = cv2.inRange(frame_gray, 210, 255)
    
    binary = cv2.resize(binary, SIZE)
    #cv2.imshow("Binary", binary)


    binary_visual = binary.copy()

    
    cv2.polylines(binary_visual, [np.array(TRAP, dtype=np.int32)], True, 255, 2)
    #cv2.imshow("TRAP", binary_visual )


    M = cv2.getPerspectiveTransform(TRAP, RECT)

    perspective = cv2.warpPerspective(binary, M, SIZE, flags=cv2.INTER_LINEAR)
    
   # cv2.imshow("Perspective", perspective)
    



    hist = np.sum(perspective[0:200], axis=0) #axis
    
    center = hist.shape[0] // 2
    #print('center',center)

    hist_l = hist[:center]
    hist_r = hist[center:]
    # print(f""" hist_l={hist_l} 
    # hist_r={hist_r} """)

    ind_left = np.argmax(hist_l)
    ind_right = np.argmax(hist_r) + center
    #print(ind_left, ind_right)

    out = perspective.copy()
    

    cv2.line(out, (ind_left, 0), (ind_left, 299), 255, 2)
    cv2.line(out, (ind_right, 0), (ind_right, 299), 255, 2)
    #cv2.imshow("Lines", out)

    center_road = (ind_left + ind_right) // 2
    #print("center_road",center_road)
   

    Error = center_road - center
    #print('Error',Error)

    angle = 1400 + (Error*10)
    print(angle)
    
    #time.sleep(0.1)


    

    
    pi.set_servo_pulsewidth(STEER, int(angle))
    time.sleep(0.2)
    #pi.set_servo_pulsewidth(ESC, 1555)


    if cv2.waitKey(1)==ord("q"):
        break


    if cv2.waitKey(1)==ord("a"):
        os.system("sudo killall pigpiod")
        print("sudo killall pigpiod")
        break