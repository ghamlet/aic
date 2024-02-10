import time

import cv2
import numpy as np

#from arduino import Arduino
import utils 


CAR_SPEED = 1430
ARDUINO_PORT = '/dev/ttyUSB0'
CAMERA_ID = '/dev/video0'

KP = 0.55  # 0.22 0.32 0.42
KD = 0.25  # 0.17
last = 0

SIZE = (533, 300)

RECT = np.float32([[0, SIZE[1]],
                   [SIZE[0], SIZE[1]],
                   [SIZE[0], 0],
                   [0, 0]])

TRAP = np.float32([[10, 299],
                   [523, 299],
                   [440, 200],
                   [93, 200]])

src_draw = np.array(TRAP, dtype=np.int32)

# OPENCV PARAMS
THRESHOLD = 200
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#arduino = Arduino(ARDUINO_PORT, baudrate=115200, timeout=10)
time.sleep(1)

#cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_V4L2)
cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#arduino.set_speed(CAR_SPEED)

last_err = 0
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img = cv2.resize(frame, SIZE)
        binary = utils.binarize_exp(img)

        #utils.cross_center_path_v2(binary)


        perspective = utils.trans_perspective(binary, TRAP, RECT, SIZE, d=1)
        
        #print("Stop line",utils.detect_stop(perspective))

        left, right = utils.centre_mass(perspective, d=1)
        
        err = 0 - ((left + right) // 2 - SIZE[0] // 2)
        if abs(right - left) < 100:
            err = last_err

        angle = int(90 + KP * err + KD * (err - last_err))

        if angle < 60:
            angle = 60
        elif angle > 120:
            angle = 120

        last_err = err
        print(f'angle={angle}')
       # arduino.set_angle(angle)
except KeyboardInterrupt as e:
    print('Program stopped!', e)


# arduino.stop()
# arduino.set_angle(90)
cap.release()
