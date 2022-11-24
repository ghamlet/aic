import cv2 
#cv2 = cv
import numpy as np
import time
import os
import pigpio
#test_git

os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)

ESC = 17 # драйвер двигателя, смотри на номера после GPIO
STEER = 18 # сервопривод

pi = pigpio.pi()
time.sleep(1)
pi.set_servo_pulsewidth(ESC, 0)
pi.set_servo_pulsewidth(STEER, 0)
time.sleep(2)
print("podau signal")
pi.set_servo_pulsewidth(ESC, 1500)
time.sleep(2)

cap = cv2.VideoCapture(1)

ESCAPE = 27
key = 1

RECT = np.float32([[0, 299],
                   [399, 299],
                   [399, 0],
                   [0, 0]])

TRAP = np.float32([[0, 299],
                   [399, 299],
                   [320, 200],
                   [80, 200]])

src_draw = np.array(TRAP, dtype=np.int32)

SIZE = (400, 300)

while (key != ESCAPE):
    ret, frame = cap.read()

   # if ret == False:
    #    print("End of File")
     #   break
    cv2.imshow("frame", frame)
    #key = cv2.waitKey(10)

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Gray", frame_gray)

    binary = cv2.inRange(frame_gray, 170, 255)
    #cv2.imshow("Binary", binary)

    binary = cv2.resize(binary, SIZE)

    binary_visual = binary.copy()
    #cv2.polylines(binary_visual, [src_draw], True, 255)
    #cv2.imshow("TRAP", binary_visual)

    M = cv2.getPerspectiveTransform(TRAP, RECT)
    perspective = cv2.warpPerspective(binary, M, SIZE, flags=cv2.INTER_LINEAR)
    #cv2.imshow("Perspective", perspective)

    hist = np.sum(perspective, axis=0)
    #print(hist)
    center = hist.shape[0] // 2

    hist_l = hist[:center]
    hist_r = hist[center:]

    ind_left = np.argmax(hist_l)
    ind_right = np.argmax(hist_r) + center

    print(ind_left, ind_right)

    out = perspective.copy()
    # cv2.line(out, (ind_left, 0), (ind_left, 299), 50, 2)
    # cv2.line(out, (ind_right, 0), (ind_right, 299), 50, 2)
    # cv2.imshow("Lines", out)

    center_road = (ind_left + ind_right) // 2
    Error = center_road - center

    print(Error)
    angle = 110 - (Error*0.5)
    if angle > 110 + 22:
        angle = 110 + 22
    if angle < 110 - 22:
        angle = 110 - 22

    pi.set_servo_pulsewidth(STEER, int(16.66666 * angle))
    pi.set_servo_pulsewidth(ESC, 1555)

cv2.destroyAllWindows()
cap.release()